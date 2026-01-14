--
-- PostgreSQL database dump
--

\restrict YbeGzjdcDByvR8O2TQlOfURcKKBBoG7WzuucYr8RhT12CzqmF2R7PUn8bIKnL4L

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

-- Started on 2026-01-13 13:17:34

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 305 (class 1255 OID 17369)
-- Name: sp_get_timeline_carga(bigint); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.sp_get_timeline_carga(p_idcargapatriarca bigint) RETURNS TABLE(idstatuscarga smallint, strdescricao text, datregistro timestamp with time zone, strmensagem text)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT d.idStatusCarga,
           s.strDescricao,
           d.datRegistro,
           d.strMensagem
      FROM TBLDetalheStatusCarga d
      JOIN TBLStatusCarga s
        ON s.idStatusCarga = d.idStatusCarga
     WHERE d.idCargaPatriarca = p_idCargaPatriarca
     ORDER BY d.datRegistro;
END;
$$;


ALTER FUNCTION public.sp_get_timeline_carga(p_idcargapatriarca bigint) OWNER TO postgres;

--
-- TOC entry 299 (class 1255 OID 17363)
-- Name: sp_insert_carga_patriarca(bigint, bigint, integer, integer, text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.sp_insert_carga_patriarca(p_idpatriarca bigint, p_idtokenenviocarga bigint, p_idstatuscarga integer, p_idtipocarga integer, p_strmensagemretorno text) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE v_id BIGINT;
BEGIN
    INSERT INTO TBLCargaPatriarca (
        idPatriarca,
        idTokenEnvioCarga,
        idStatusCarga,
        idTipoCarga,
        strMensagemRetorno
    ) VALUES (
        p_idPatriarca,
        p_idTokenEnvioCarga,
        p_idStatusCarga,
        p_idTipoCarga,
        p_strMensagemRetorno
    )
    RETURNING idCargaPatriarca INTO v_id;

    RETURN v_id;
END;
$$;


ALTER FUNCTION public.sp_insert_carga_patriarca(p_idpatriarca bigint, p_idtokenenviocarga bigint, p_idstatuscarga integer, p_idtipocarga integer, p_strmensagemretorno text) OWNER TO postgres;

--
-- TOC entry 290 (class 1255 OID 17356)
-- Name: sp_insert_classificacao_usuario(integer, text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.sp_insert_classificacao_usuario(p_idclassificacaousuario integer, p_strdescricao text) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_id BIGINT;
BEGIN
    IF p_idclassificacaousuario <= 0 THEN
        RETURN -1;
    END IF;

    INSERT INTO TBLClassificacaoUsuario (idClassificacaoUsuario, strDescricao)
    VALUES (p_idclassificacaousuario, p_strdescricao)
    RETURNING idClassificacaoUsuario INTO v_id;

    RETURN v_id;
END;
$$;


ALTER FUNCTION public.sp_insert_classificacao_usuario(p_idclassificacaousuario integer, p_strdescricao text) OWNER TO postgres;

--
-- TOC entry 293 (class 1255 OID 17357)
-- Name: sp_insert_detalhe_status_carga(bigint, integer, text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.sp_insert_detalhe_status_carga(p_idcargapatriarca bigint, p_idstatuscarga integer, p_strmensagem text) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_id BIGINT;
BEGIN
    -- valida carga
    IF NOT EXISTS (
        SELECT 1 FROM TBLCargaPatriarca
         WHERE idCargaPatriarca = p_idCargaPatriarca
    ) THEN
        RETURN -1;
    END IF;

    -- valida status
    IF NOT EXISTS (
        SELECT 1 FROM TBLStatusCarga
         WHERE idStatusCarga = p_idStatusCarga
    ) THEN
        RETURN -2;
    END IF;

    INSERT INTO TBLDetalheStatusCarga (
        idCargaPatriarca,
        idStatusCarga,
        strMensagem
    ) VALUES (
        p_idCargaPatriarca,
        p_idStatusCarga,
        p_strMensagem
    )
    RETURNING idDetalheStatusCarga INTO v_id;

    RETURN v_id;
END;
$$;


ALTER FUNCTION public.sp_insert_detalhe_status_carga(p_idcargapatriarca bigint, p_idstatuscarga integer, p_strmensagem text) OWNER TO postgres;

--
-- TOC entry 300 (class 1255 OID 17364)
-- Name: sp_insert_lotacao(bigint, bigint, bigint, bigint, text, text, text, boolean, text, date, bigint); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.sp_insert_lotacao(p_idlotacaoversao bigint, p_idpatriarca bigint, p_idorgaolotacao bigint, p_idunidadelotacao bigint, p_strcpf text, p_strcargooriginal text, p_strcargonormalizado text, p_flgvalido boolean, p_strerrosvalidacao text, p_datreferencia date, p_idusuariocriacao bigint) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_id BIGINT;
    v_idOrganogramaVersao BIGINT;
BEGIN
    -- 1. valida patriarca
    IF NOT EXISTS (
        SELECT 1 FROM TBLPatriarca WHERE idPatriarca = p_idPatriarca
    ) THEN
        RETURN -1;
    END IF;

    -- 2. obtém organograma ATIVO
    SELECT idOrganogramaVersao
      INTO v_idOrganogramaVersao
      FROM TBLOrganogramaVersao
     WHERE idPatriarca = p_idPatriarca
       AND flgAtivo = TRUE;

    IF v_idOrganogramaVersao IS NULL THEN
        RETURN -2; -- sem organograma ativo
    END IF;

    -- 3. valida versão de lotação × organograma
    IF NOT EXISTS (
        SELECT 1
          FROM TBLLotacaoVersao
         WHERE idLotacaoVersao = p_idLotacaoVersao
           AND idOrganogramaVersao = v_idOrganogramaVersao
           AND idPatriarca = p_idPatriarca
    ) THEN
        RETURN -3;
    END IF;

    -- 4. insere lotação SEM permitir organograma arbitrário
    INSERT INTO TBLLotacao (
        idLotacaoVersao,
        idOrganogramaVersao,
        idPatriarca,
        idOrgaoLotacao,
        idUnidadeLotacao,
        strCpf,
        strCargoOriginal,
        strCargoNormalizado,
        flgValido,
        strErrosValidacao,
        datReferencia,
        datCriacao,
        idUsuarioCriacao
    ) VALUES (
        p_idLotacaoVersao,
        v_idOrganogramaVersao,
        p_idPatriarca,
        p_idOrgaoLotacao,
        p_idUnidadeLotacao,
        p_strCpf,
        p_strCargoOriginal,
        p_strCargoNormalizado,
        COALESCE(p_flgValido, TRUE),
        p_strErrosValidacao,
        p_datReferencia,
        now(),
        p_idUsuarioCriacao
    )
    RETURNING idLotacao INTO v_id;

    RETURN v_id;
END;
$$;


ALTER FUNCTION public.sp_insert_lotacao(p_idlotacaoversao bigint, p_idpatriarca bigint, p_idorgaolotacao bigint, p_idunidadelotacao bigint, p_strcpf text, p_strcargooriginal text, p_strcargonormalizado text, p_flgvalido boolean, p_strerrosvalidacao text, p_datreferencia date, p_idusuariocriacao bigint) OWNER TO postgres;

--
-- TOC entry 304 (class 1255 OID 17368)
-- Name: sp_insert_lotacao_inconsistencia(bigint, text, text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.sp_insert_lotacao_inconsistencia(p_idlotacao bigint, p_strtipo text, p_strdetalhe text) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE v_id BIGINT;
BEGIN
    INSERT INTO TBLLotacaoInconsistencia (
        idLotacao, strTipo, strDetalhe
    ) VALUES (
        p_idLotacao, p_strTipo, p_strDetalhe
    )
    RETURNING idInconsistencia INTO v_id;

    RETURN v_id;
END;
$$;


ALTER FUNCTION public.sp_insert_lotacao_inconsistencia(p_idlotacao bigint, p_strtipo text, p_strdetalhe text) OWNER TO postgres;

--
-- TOC entry 303 (class 1255 OID 17367)
-- Name: sp_insert_lotacao_json_orgao(bigint, bigint, bigint, bigint, jsonb); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.sp_insert_lotacao_json_orgao(p_idlotacaoversao bigint, p_idorganogramaversao bigint, p_idpatriarca bigint, p_idorgaolotacao bigint, p_jsconteudo jsonb) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE v_id BIGINT;
BEGIN
    INSERT INTO TBLLotacaoJsonOrgao (
        idLotacaoVersao,
        idOrganogramaVersao,
        idPatriarca,
        idOrgaoLotacao,
        jsConteudo
    ) VALUES (
        p_idLotacaoVersao,
        p_idOrganogramaVersao,
        p_idPatriarca,
        p_idOrgaoLotacao,
        p_jsConteudo
    )
    RETURNING idLotacaoJsonOrgao INTO v_id;

    RETURN v_id;
END;
$$;


ALTER FUNCTION public.sp_insert_lotacao_json_orgao(p_idlotacaoversao bigint, p_idorganogramaversao bigint, p_idpatriarca bigint, p_idorgaolotacao bigint, p_jsconteudo jsonb) OWNER TO postgres;

--
-- TOC entry 301 (class 1255 OID 17365)
-- Name: sp_insert_lotacao_versao(bigint, text, text, text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.sp_insert_lotacao_versao(p_idpatriarca bigint, p_strorigem text, p_strtipoarquivooriginal text, p_strnomearquivooriginal text) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_id BIGINT;
    v_idOrganogramaVersao BIGINT;
BEGIN
    -- obtém organograma ativo
    SELECT idOrganogramaVersao
      INTO v_idOrganogramaVersao
      FROM TBLOrganogramaVersao
     WHERE idPatriarca = p_idPatriarca
       AND flgAtivo = TRUE;

    IF v_idOrganogramaVersao IS NULL THEN
        RETURN -1;
    END IF;

    INSERT INTO TBLLotacaoVersao (
        idPatriarca,
        idOrganogramaVersao,
        strOrigem,
        strTipoArquivoOriginal,
        strNomeArquivoOriginal,
        datProcessamento,
        strStatusProcessamento,
        flgAtivo
    ) VALUES (
        p_idPatriarca,
        v_idOrganogramaVersao,
        p_strOrigem,
        p_strTipoArquivoOriginal,
        p_strNomeArquivoOriginal,
        now(),
        'Sucesso',
        FALSE
    )
    RETURNING idLotacaoVersao INTO v_id;

    RETURN v_id;
END;
$$;


ALTER FUNCTION public.sp_insert_lotacao_versao(p_idpatriarca bigint, p_strorigem text, p_strtipoarquivooriginal text, p_strnomearquivooriginal text) OWNER TO postgres;

--
-- TOC entry 302 (class 1255 OID 17366)
-- Name: sp_insert_organograma_json(bigint, jsonb); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.sp_insert_organograma_json(p_idorganogramaversao bigint, p_jsconteudo jsonb) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE v_id BIGINT;
BEGIN
    INSERT INTO TBLOrganogramaJson (idOrganogramaVersao, jsConteudo)
    VALUES (p_idOrganogramaVersao, p_jsConteudo)
    RETURNING idOrganogramaJson INTO v_id;

    RETURN v_id;
END;
$$;


ALTER FUNCTION public.sp_insert_organograma_json(p_idorganogramaversao bigint, p_jsconteudo jsonb) OWNER TO postgres;

--
-- TOC entry 294 (class 1255 OID 17358)
-- Name: sp_insert_patriarca(uuid, text, text, integer, bigint); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.sp_insert_patriarca(p_idexternopatriarca uuid, p_strsiglapatriarca text, p_strnome text, p_idstatusprogresso integer, p_idusuariocriacao bigint) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_id BIGINT;
BEGIN
	IF NOT EXISTS (SELECT 1 FROM TBLStatusProgresso WHERE idStatusProgresso = p_idStatusProgresso) THEN
	    RETURN -1;
	END IF;
	
	IF NOT EXISTS (SELECT 1 FROM TBLUsuario WHERE idUsuario = p_idUsuarioCriacao) THEN
	    RETURN -2;
	END IF;

    INSERT INTO TBLPatriarca(
        idExternoPatriarca, strSiglaPatriarca, strNome,
        idStatusProgresso, datCriacao, idUsuarioCriacao
    ) VALUES (
        p_idExternoPatriarca, p_strSiglaPatriarca, p_strNome,
        p_idStatusProgresso, now(), p_idUsuarioCriacao
    )
    RETURNING idPatriarca INTO v_id;

    RETURN v_id;
END;
$$;


ALTER FUNCTION public.sp_insert_patriarca(p_idexternopatriarca uuid, p_strsiglapatriarca text, p_strnome text, p_idstatusprogresso integer, p_idusuariocriacao bigint) OWNER TO postgres;

--
-- TOC entry 296 (class 1255 OID 17360)
-- Name: sp_insert_status_carga(integer, text, boolean); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.sp_insert_status_carga(p_idstatuscarga integer, p_strdescricao text, p_flgsucesso boolean) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE v_id BIGINT;
BEGIN
    IF p_idstatuscarga <= 0 THEN
        RETURN -1;
    END IF;

    INSERT INTO TBLStatusCarga (idStatusCarga, strDescricao, flgSucesso)
    VALUES (p_idstatuscarga, p_strdescricao, p_flgSucesso)
    RETURNING idStatusCarga INTO v_id;

    RETURN v_id;
END;
$$;


ALTER FUNCTION public.sp_insert_status_carga(p_idstatuscarga integer, p_strdescricao text, p_flgsucesso boolean) OWNER TO postgres;

--
-- TOC entry 308 (class 1255 OID 17374)
-- Name: sp_insert_status_carga(integer, text, integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.sp_insert_status_carga(p_idstatuscarga integer, p_strdescricao text, p_flgsucesso integer) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE v_id BIGINT;
BEGIN
    IF p_idstatuscarga <= 0 THEN
        RETURN -1;
    END IF;

    INSERT INTO TBLStatusCarga (idStatusCarga, strDescricao, flgSucesso)
    VALUES (p_idstatuscarga, p_strdescricao, p_flgSucesso)
    RETURNING idStatusCarga INTO v_id;

    RETURN v_id;
END;
$$;


ALTER FUNCTION public.sp_insert_status_carga(p_idstatuscarga integer, p_strdescricao text, p_flgsucesso integer) OWNER TO postgres;

--
-- TOC entry 289 (class 1255 OID 17355)
-- Name: sp_insert_status_usuario(integer, text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.sp_insert_status_usuario(p_idstatususuario integer, p_strdescricao text) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_id BIGINT;
BEGIN
    IF p_idstatususuario <= 0 THEN
        RETURN -1;
    END IF;

    INSERT INTO TBLStatusUsuario (idStatusUsuario, strDescricao)
    VALUES (p_idstatususuario, p_strdescricao)
    RETURNING idStatusUsuario INTO v_id;

    RETURN v_id;
END;
$$;


ALTER FUNCTION public.sp_insert_status_usuario(p_idstatususuario integer, p_strdescricao text) OWNER TO postgres;

--
-- TOC entry 297 (class 1255 OID 17361)
-- Name: sp_insert_tipo_carga(integer, text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.sp_insert_tipo_carga(p_idtipocarga integer, p_strdescricao text) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE v_id BIGINT;
BEGIN
    IF p_idtipocarga <= 0 THEN
        RETURN -1;
    END IF;

    INSERT INTO TBLTipoCarga (idTipoCarga, strDescricao)
    VALUES (p_idtipocarga, p_strdescricao)
    RETURNING idTipoCarga INTO v_id;

    RETURN v_id;
END;
$$;


ALTER FUNCTION public.sp_insert_tipo_carga(p_idtipocarga integer, p_strdescricao text) OWNER TO postgres;

--
-- TOC entry 295 (class 1255 OID 17359)
-- Name: sp_insert_tipo_usuario(integer, text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.sp_insert_tipo_usuario(p_idtipousuario integer, p_strdescricao text) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE v_id BIGINT;
BEGIN
    IF p_idtipousuario <= 0 THEN
        RETURN -1;
    END IF;

    INSERT INTO TBLTipoUsuario (idTipoUsuario, strDescricao)
    VALUES (p_idtipousuario, p_strdescricao)
    RETURNING idTipoUsuario INTO v_id;

    RETURN v_id;
END;
$$;


ALTER FUNCTION public.sp_insert_tipo_usuario(p_idtipousuario integer, p_strdescricao text) OWNER TO postgres;

--
-- TOC entry 298 (class 1255 OID 17362)
-- Name: sp_insert_token_envio_carga(bigint, integer, text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.sp_insert_token_envio_carga(p_idpatriarca bigint, p_idstatustokenenviocarga integer, p_strtokenretorno text) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE v_id BIGINT;
BEGIN
    INSERT INTO TBLTokenEnvioCarga (
        idPatriarca,
        idStatusTokenEnvioCarga,
        strTokenRetorno
    ) VALUES (
        p_idPatriarca,
        p_idStatusTokenEnvioCarga,
        p_strTokenRetorno
    )
    RETURNING idTokenEnvioCarga INTO v_id;

    RETURN v_id;
END;
$$;


ALTER FUNCTION public.sp_insert_token_envio_carga(p_idpatriarca bigint, p_idstatustokenenviocarga integer, p_strtokenretorno text) OWNER TO postgres;

--
-- TOC entry 291 (class 1255 OID 17370)
-- Name: sp_insert_usuario(text, text, text, smallint, smallint, smallint, bigint); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.sp_insert_usuario(p_strnome text, p_stremail text, p_strsenha text, p_idstatususuario smallint, p_idtipousuario smallint, p_idclassificacaousuario smallint, p_idusuariocriacao bigint) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_id BIGINT;
BEGIN
    -- Validações básicas
    IF p_strNome IS NULL OR p_strEmail IS NULL OR p_strSenha IS NULL THEN
        RAISE EXCEPTION 'Nome, e-mail e senha são obrigatórios';
    END IF;

    -- Validação das FKs
    IF NOT EXISTS (SELECT 1 FROM TBLStatusUsuario WHERE idStatusUsuario = p_idStatusUsuario) THEN
        RAISE EXCEPTION 'Status de usuário inválido';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM TBLTipoUsuario WHERE idTipoUsuario = p_idTipoUsuario) THEN
        RAISE EXCEPTION 'Tipo de usuário inválido';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM TBLClassificacaoUsuario WHERE idClassificacaoUsuario = p_idClassificacaoUsuario) THEN
        RAISE EXCEPTION 'Classificação de usuário inválida';
    END IF;

    INSERT INTO TBLUsuario (
        strNome,
        strEmail,
        strSenha,
        idStatusUsuario,
        idTipoUsuario,
        idClassificacaoUsuario,
        datacriacao,
        idUsuarioCriacao
    ) VALUES (
        p_strNome,
        p_strEmail,
        p_strSenha,
        p_idStatusUsuario,
        p_idTipoUsuario,
        p_idClassificacaoUsuario,
        now(),
        p_idUsuarioCriacao
    )
    RETURNING idUsuario INTO v_id;

    RETURN v_id;
END;
$$;


ALTER FUNCTION public.sp_insert_usuario(p_strnome text, p_stremail text, p_strsenha text, p_idstatususuario smallint, p_idtipousuario smallint, p_idclassificacaousuario smallint, p_idusuariocriacao bigint) OWNER TO postgres;

--
-- TOC entry 307 (class 1255 OID 17354)
-- Name: sp_set_organograma_versao_ativa(bigint, bigint); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.sp_set_organograma_versao_ativa(p_idpatriarca bigint, p_idorganogramaversao bigint) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_exists INTEGER;
BEGIN
    -- valida patriarca
    SELECT 1 INTO v_exists
      FROM TBLPatriarca
     WHERE idPatriarca = p_idPatriarca;

    IF v_exists IS NULL THEN
        RETURN -1;
    END IF;

    -- valida versão
    SELECT 1 INTO v_exists
      FROM TBLOrganogramaVersao
     WHERE idOrganogramaVersao = p_idOrganogramaVersao;

    IF v_exists IS NULL THEN
        RETURN -2;
    END IF;

    -- valida vínculo versão × patriarca
    SELECT 1 INTO v_exists
      FROM TBLOrganogramaVersao
     WHERE idOrganogramaVersao = p_idOrganogramaVersao
       AND idPatriarca = p_idPatriarca;

    IF v_exists IS NULL THEN
        RETURN -3;
    END IF;

    -- desativa versões atuais
    UPDATE TBLOrganogramaVersao
       SET flgAtivo = FALSE
     WHERE idPatriarca = p_idPatriarca
       AND flgAtivo = TRUE;

    -- ativa versão desejada
    UPDATE TBLOrganogramaVersao
       SET flgAtivo = TRUE
     WHERE idOrganogramaVersao = p_idOrganogramaVersao;

    RETURN p_idOrganogramaVersao;
END;
$$;


ALTER FUNCTION public.sp_set_organograma_versao_ativa(p_idpatriarca bigint, p_idorganogramaversao bigint) OWNER TO postgres;

--
-- TOC entry 306 (class 1255 OID 17353)
-- Name: sp_update_patriarca(bigint, text, integer, bigint); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.sp_update_patriarca(p_idpatriarca bigint, p_strnome text, p_idstatusprogresso integer, p_idusuarioalteracao bigint) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_exists INTEGER;
BEGIN
    -- valida patriarca
    SELECT 1 INTO v_exists
      FROM TBLPatriarca
     WHERE idPatriarca = p_idPatriarca;

    IF v_exists IS NULL THEN
        RETURN -1;
    END IF;

    -- valida status de progresso (se informado)
    IF p_idStatusProgresso IS NOT NULL AND NOT EXISTS (
        SELECT 1 FROM TBLStatusProgresso
         WHERE idStatusProgresso = p_idStatusProgresso
    ) THEN
        RETURN -2;
    END IF;

    -- valida usuário de alteração (se informado)
    IF p_idUsuarioAlteracao IS NOT NULL AND NOT EXISTS (
        SELECT 1 FROM TBLUsuario
         WHERE idUsuario = p_idUsuarioAlteracao
    ) THEN
        RETURN -3;
    END IF;

    UPDATE TBLPatriarca
       SET strNome            = COALESCE(p_strNome, strNome),
           idStatusProgresso  = COALESCE(p_idStatusProgresso, idStatusProgresso),
           datAlteracao       = now(),
           idUsuarioAlteracao = COALESCE(p_idUsuarioAlteracao, idUsuarioAlteracao)
     WHERE idPatriarca = p_idPatriarca;

    RETURN p_idPatriarca;
END;
$$;


ALTER FUNCTION public.sp_update_patriarca(p_idpatriarca bigint, p_strnome text, p_idstatusprogresso integer, p_idusuarioalteracao bigint) OWNER TO postgres;

--
-- TOC entry 292 (class 1255 OID 17371)
-- Name: sp_update_usuario(bigint, text, text, text, smallint, smallint, smallint, bigint); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.sp_update_usuario(p_idusuario bigint, p_strnome text, p_stremail text, p_strsenha text, p_idstatususuario smallint, p_idtipousuario smallint, p_idclassificacaousuario smallint, p_idusuarioalteracao bigint) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    UPDATE TBLUsuario
       SET strNome                = COALESCE(p_strNome, strNome),
           strEmail               = COALESCE(p_strEmail, strEmail),
           strSenha               = COALESCE(p_strSenha, strSenha),
           idStatusUsuario        = COALESCE(p_idStatusUsuario, idStatusUsuario),
           idTipoUsuario          = COALESCE(p_idTipoUsuario, idTipoUsuario),
           idClassificacaoUsuario = COALESCE(p_idClassificacaoUsuario, idClassificacaoUsuario),
           data_alteracao         = now(),
           idUsuarioAlteracao     = p_idUsuarioAlteracao
     WHERE idUsuario = p_idUsuario;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Usuário não encontrado';
    END IF;
END;
$$;


ALTER FUNCTION public.sp_update_usuario(p_idusuario bigint, p_strnome text, p_stremail text, p_strsenha text, p_idstatususuario smallint, p_idtipousuario smallint, p_idclassificacaousuario smallint, p_idusuarioalteracao bigint) OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 265 (class 1259 OID 17854)
-- Name: accounts_attribute; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts_attribute (
    id bigint NOT NULL,
    key character varying(100) NOT NULL,
    value character varying(255) NOT NULL,
    aplicacao_id integer,
    user_id bigint NOT NULL
);


ALTER TABLE public.accounts_attribute OWNER TO postgres;

--
-- TOC entry 264 (class 1259 OID 17853)
-- Name: accounts_attribute_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.accounts_attribute ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.accounts_attribute_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 263 (class 1259 OID 17844)
-- Name: accounts_role; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts_role (
    id bigint NOT NULL,
    nomeperfil character varying(100) NOT NULL,
    codigoperfil character varying(100) NOT NULL,
    aplicacao_id integer NOT NULL
);


ALTER TABLE public.accounts_role OWNER TO postgres;

--
-- TOC entry 262 (class 1259 OID 17843)
-- Name: accounts_role_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.accounts_role ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.accounts_role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 267 (class 1259 OID 17864)
-- Name: accounts_userrole; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts_userrole (
    id bigint NOT NULL,
    aplicacao_id integer NOT NULL,
    role_id bigint NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.accounts_userrole OWNER TO postgres;

--
-- TOC entry 266 (class 1259 OID 17863)
-- Name: accounts_userrole_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.accounts_userrole ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.accounts_userrole_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 259 (class 1259 OID 17795)
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- TOC entry 258 (class 1259 OID 17794)
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 261 (class 1259 OID 17805)
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- TOC entry 260 (class 1259 OID 17804)
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 257 (class 1259 OID 17785)
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- TOC entry 256 (class 1259 OID 17784)
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 270 (class 1259 OID 17942)
-- Name: authtoken_token; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.authtoken_token (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.authtoken_token OWNER TO postgres;

--
-- TOC entry 272 (class 1259 OID 17959)
-- Name: db_service_appclient; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.db_service_appclient (
    id bigint NOT NULL,
    client_id character varying(100) NOT NULL,
    client_secret_hash character varying(255) NOT NULL,
    is_active boolean NOT NULL,
    aplicacao_id integer NOT NULL
);


ALTER TABLE public.db_service_appclient OWNER TO postgres;

--
-- TOC entry 271 (class 1259 OID 17958)
-- Name: db_service_appclient_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.db_service_appclient ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.db_service_appclient_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 269 (class 1259 OID 17916)
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- TOC entry 268 (class 1259 OID 17915)
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 255 (class 1259 OID 17773)
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- TOC entry 254 (class 1259 OID 17772)
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 253 (class 1259 OID 17761)
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- TOC entry 252 (class 1259 OID 17760)
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 273 (class 1259 OID 17979)
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- TOC entry 251 (class 1259 OID 17738)
-- Name: tblaplicacao; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tblaplicacao (
    idaplicacao bigint CONSTRAINT tblaplicacao_idapplication_not_null NOT NULL,
    codigointerno character varying(50) CONSTRAINT tblaplicacao_code_not_null NOT NULL,
    nomeaplicacao character varying(200) CONSTRAINT tblaplicacao_name_not_null NOT NULL,
    base_url character varying(500)
);


ALTER TABLE public.tblaplicacao OWNER TO postgres;

--
-- TOC entry 250 (class 1259 OID 17737)
-- Name: tblaplicacao_idapplication_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tblaplicacao_idapplication_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tblaplicacao_idapplication_seq OWNER TO postgres;

--
-- TOC entry 5478 (class 0 OID 0)
-- Dependencies: 250
-- Name: tblaplicacao_idapplication_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tblaplicacao_idapplication_seq OWNED BY public.tblaplicacao.idaplicacao;


--
-- TOC entry 233 (class 1259 OID 17038)
-- Name: tblcargapatriarca; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tblcargapatriarca (
    idcargapatriarca bigint NOT NULL,
    idpatriarca bigint NOT NULL,
    idtokenenviocarga bigint NOT NULL,
    idstatuscarga smallint NOT NULL,
    idtipocarga smallint NOT NULL,
    strmensagemretorno text,
    datdatahorainicio timestamp with time zone DEFAULT now() NOT NULL,
    datdatahorafim timestamp with time zone
);


ALTER TABLE public.tblcargapatriarca OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 17037)
-- Name: tblcargapatriarca_idcargapatriarca_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tblcargapatriarca_idcargapatriarca_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tblcargapatriarca_idcargapatriarca_seq OWNER TO postgres;

--
-- TOC entry 5479 (class 0 OID 0)
-- Dependencies: 232
-- Name: tblcargapatriarca_idcargapatriarca_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tblcargapatriarca_idcargapatriarca_seq OWNED BY public.tblcargapatriarca.idcargapatriarca;


--
-- TOC entry 221 (class 1259 OID 16893)
-- Name: tblclassificacaousuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tblclassificacaousuario (
    idclassificacaousuario smallint NOT NULL,
    strdescricao character varying(100) NOT NULL
);


ALTER TABLE public.tblclassificacaousuario OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 17075)
-- Name: tbldetalhestatuscarga; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbldetalhestatuscarga (
    iddetalhestatuscarga bigint NOT NULL,
    idcargapatriarca bigint NOT NULL,
    idstatuscarga smallint NOT NULL,
    datregistro timestamp with time zone DEFAULT now() NOT NULL,
    strmensagem text
);


ALTER TABLE public.tbldetalhestatuscarga OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 17074)
-- Name: tbldetalhestatuscarga_iddetalhestatuscarga_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tbldetalhestatuscarga_iddetalhestatuscarga_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tbldetalhestatuscarga_iddetalhestatuscarga_seq OWNER TO postgres;

--
-- TOC entry 5480 (class 0 OID 0)
-- Dependencies: 234
-- Name: tbldetalhestatuscarga_iddetalhestatuscarga_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tbldetalhestatuscarga_iddetalhestatuscarga_seq OWNED BY public.tbldetalhestatuscarga.iddetalhestatuscarga;


--
-- TOC entry 245 (class 1259 OID 17223)
-- Name: tbllotacao; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbllotacao (
    idlotacao bigint NOT NULL,
    idlotacaoversao bigint NOT NULL,
    idorganogramaversao bigint NOT NULL,
    idpatriarca bigint NOT NULL,
    idorgaolotacao bigint NOT NULL,
    idunidadelotacao bigint,
    strcpf character varying(14) NOT NULL,
    strcargooriginal character varying(255),
    strcargonormalizado character varying(255),
    flgvalido boolean DEFAULT true NOT NULL,
    strerrosvalidacao text,
    datreferencia date,
    datcriacao timestamp with time zone DEFAULT now() NOT NULL,
    idusuariocriacao bigint,
    datalteracao timestamp with time zone,
    idusuarioalteracao bigint
);


ALTER TABLE public.tbllotacao OWNER TO postgres;

--
-- TOC entry 244 (class 1259 OID 17222)
-- Name: tbllotacao_idlotacao_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tbllotacao_idlotacao_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tbllotacao_idlotacao_seq OWNER TO postgres;

--
-- TOC entry 5481 (class 0 OID 0)
-- Dependencies: 244
-- Name: tbllotacao_idlotacao_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tbllotacao_idlotacao_seq OWNED BY public.tbllotacao.idlotacao;


--
-- TOC entry 249 (class 1259 OID 17320)
-- Name: tbllotacaoinconsistencia; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbllotacaoinconsistencia (
    idinconsistencia bigint NOT NULL,
    idlotacao bigint NOT NULL,
    strtipo character varying(100) NOT NULL,
    strdetalhe text NOT NULL,
    datregistro timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.tbllotacaoinconsistencia OWNER TO postgres;

--
-- TOC entry 248 (class 1259 OID 17319)
-- Name: tbllotacaoinconsistencia_idinconsistencia_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tbllotacaoinconsistencia_idinconsistencia_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tbllotacaoinconsistencia_idinconsistencia_seq OWNER TO postgres;

--
-- TOC entry 5482 (class 0 OID 0)
-- Dependencies: 248
-- Name: tbllotacaoinconsistencia_idinconsistencia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tbllotacaoinconsistencia_idinconsistencia_seq OWNED BY public.tbllotacaoinconsistencia.idinconsistencia;


--
-- TOC entry 247 (class 1259 OID 17280)
-- Name: tbllotacaojsonorgao; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbllotacaojsonorgao (
    idlotacaojsonorgao bigint NOT NULL,
    idlotacaoversao bigint NOT NULL,
    idorganogramaversao bigint NOT NULL,
    idpatriarca bigint NOT NULL,
    idorgaolotacao bigint NOT NULL,
    jsconteudo jsonb NOT NULL,
    datcriacao timestamp with time zone DEFAULT now() NOT NULL,
    datenvioapi timestamp with time zone,
    strstatusenvio character varying(30),
    strmensagemretorno text
);


ALTER TABLE public.tbllotacaojsonorgao OWNER TO postgres;

--
-- TOC entry 246 (class 1259 OID 17279)
-- Name: tbllotacaojsonorgao_idlotacaojsonorgao_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tbllotacaojsonorgao_idlotacaojsonorgao_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tbllotacaojsonorgao_idlotacaojsonorgao_seq OWNER TO postgres;

--
-- TOC entry 5483 (class 0 OID 0)
-- Dependencies: 246
-- Name: tbllotacaojsonorgao_idlotacaojsonorgao_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tbllotacaojsonorgao_idlotacaojsonorgao_seq OWNED BY public.tbllotacaojsonorgao.idlotacaojsonorgao;


--
-- TOC entry 243 (class 1259 OID 17192)
-- Name: tbllotacaoversao; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbllotacaoversao (
    idlotacaoversao bigint NOT NULL,
    idpatriarca bigint NOT NULL,
    idorganogramaversao bigint NOT NULL,
    strorigem character varying(50) NOT NULL,
    strtipoarquivooriginal character varying(20),
    strnomearquivooriginal character varying(255),
    datprocessamento timestamp with time zone DEFAULT now() NOT NULL,
    strstatusprocessamento character varying(30) DEFAULT 'Sucesso'::character varying NOT NULL,
    strmensagemprocessamento text,
    flgativo boolean DEFAULT false NOT NULL
);


ALTER TABLE public.tbllotacaoversao OWNER TO postgres;

--
-- TOC entry 242 (class 1259 OID 17191)
-- Name: tbllotacaoversao_idlotacaoversao_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tbllotacaoversao_idlotacaoversao_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tbllotacaoversao_idlotacaoversao_seq OWNER TO postgres;

--
-- TOC entry 5484 (class 0 OID 0)
-- Dependencies: 242
-- Name: tbllotacaoversao_idlotacaoversao_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tbllotacaoversao_idlotacaoversao_seq OWNED BY public.tbllotacaoversao.idlotacaoversao;


--
-- TOC entry 241 (class 1259 OID 17172)
-- Name: tblorganogramajson; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tblorganogramajson (
    idorganogramajson bigint NOT NULL,
    idorganogramaversao bigint NOT NULL,
    jsconteudo jsonb NOT NULL,
    datcriacao timestamp with time zone DEFAULT now() NOT NULL,
    datenvioapi timestamp with time zone,
    strstatusenvio character varying(30),
    strmensagemretorno text
);


ALTER TABLE public.tblorganogramajson OWNER TO postgres;

--
-- TOC entry 240 (class 1259 OID 17171)
-- Name: tblorganogramajson_idorganogramajson_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tblorganogramajson_idorganogramajson_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tblorganogramajson_idorganogramajson_seq OWNER TO postgres;

--
-- TOC entry 5485 (class 0 OID 0)
-- Dependencies: 240
-- Name: tblorganogramajson_idorganogramajson_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tblorganogramajson_idorganogramajson_seq OWNED BY public.tblorganogramajson.idorganogramajson;


--
-- TOC entry 237 (class 1259 OID 17102)
-- Name: tblorganogramaversao; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tblorganogramaversao (
    idorganogramaversao bigint NOT NULL,
    idpatriarca bigint NOT NULL,
    strorigem character varying(50) NOT NULL,
    strtipoarquivooriginal character varying(20),
    strnomearquivooriginal character varying(255),
    datprocessamento timestamp with time zone DEFAULT now() NOT NULL,
    strstatusprocessamento character varying(30) DEFAULT 'Sucesso'::character varying NOT NULL,
    strmensagemprocessamento text,
    flgativo boolean DEFAULT false NOT NULL
);


ALTER TABLE public.tblorganogramaversao OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 17101)
-- Name: tblorganogramaversao_idorganogramaversao_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tblorganogramaversao_idorganogramaversao_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tblorganogramaversao_idorganogramaversao_seq OWNER TO postgres;

--
-- TOC entry 5486 (class 0 OID 0)
-- Dependencies: 236
-- Name: tblorganogramaversao_idorganogramaversao_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tblorganogramaversao_idorganogramaversao_seq OWNED BY public.tblorganogramaversao.idorganogramaversao;


--
-- TOC entry 239 (class 1259 OID 17126)
-- Name: tblorgaounidade; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tblorgaounidade (
    idorgaounidade bigint NOT NULL,
    idorganogramaversao bigint NOT NULL,
    idpatriarca bigint NOT NULL,
    strnome character varying(255) NOT NULL,
    strsigla character varying(50) NOT NULL,
    idorgaounidadepai bigint,
    strnumerohierarquia character varying(50),
    intnivelhierarquia integer,
    flgativo boolean DEFAULT true NOT NULL,
    datcriacao timestamp with time zone DEFAULT now() NOT NULL,
    idusuariocriacao bigint,
    datalteracao timestamp with time zone,
    idusuarioalteracao bigint
);


ALTER TABLE public.tblorgaounidade OWNER TO postgres;

--
-- TOC entry 238 (class 1259 OID 17125)
-- Name: tblorgaounidade_idorgaounidade_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tblorgaounidade_idorgaounidade_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tblorgaounidade_idorgaounidade_seq OWNER TO postgres;

--
-- TOC entry 5487 (class 0 OID 0)
-- Dependencies: 238
-- Name: tblorgaounidade_idorgaounidade_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tblorgaounidade_idorgaounidade_seq OWNED BY public.tblorgaounidade.idorgaounidade;


--
-- TOC entry 226 (class 1259 OID 16953)
-- Name: tblpatriarca; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tblpatriarca (
    idpatriarca bigint NOT NULL,
    idexternopatriarca uuid NOT NULL,
    strsiglapatriarca character varying(20) NOT NULL,
    strnome character varying(255) NOT NULL,
    idstatusprogresso smallint NOT NULL,
    datcriacao timestamp with time zone DEFAULT now() NOT NULL,
    idusuariocriacao bigint NOT NULL,
    datalteracao timestamp with time zone,
    idusuarioalteracao bigint
);


ALTER TABLE public.tblpatriarca OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16952)
-- Name: tblpatriarca_idpatriarca_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tblpatriarca_idpatriarca_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tblpatriarca_idpatriarca_seq OWNER TO postgres;

--
-- TOC entry 5488 (class 0 OID 0)
-- Dependencies: 225
-- Name: tblpatriarca_idpatriarca_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tblpatriarca_idpatriarca_seq OWNED BY public.tblpatriarca.idpatriarca;


--
-- TOC entry 231 (class 1259 OID 17029)
-- Name: tblstatuscarga; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tblstatuscarga (
    idstatuscarga smallint NOT NULL,
    strdescricao character varying(150) NOT NULL,
    flgsucesso integer NOT NULL
);


ALTER TABLE public.tblstatuscarga OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 16945)
-- Name: tblstatusprogresso; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tblstatusprogresso (
    idstatusprogresso smallint NOT NULL,
    strdescricao character varying(100) NOT NULL
);


ALTER TABLE public.tblstatusprogresso OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16989)
-- Name: tblstatustokenenviocarga; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tblstatustokenenviocarga (
    idstatustokenenviocarga smallint NOT NULL,
    strdescricao character varying(100) NOT NULL
);


ALTER TABLE public.tblstatustokenenviocarga OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16879)
-- Name: tblstatususuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tblstatususuario (
    idstatususuario smallint NOT NULL,
    strdescricao character varying(100) NOT NULL
);


ALTER TABLE public.tblstatususuario OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 17022)
-- Name: tbltipocarga; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbltipocarga (
    idtipocarga smallint NOT NULL,
    strdescricao character varying(100) NOT NULL
);


ALTER TABLE public.tbltipocarga OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16886)
-- Name: tbltipousuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbltipousuario (
    idtipousuario smallint NOT NULL,
    strdescricao character varying(100) NOT NULL
);


ALTER TABLE public.tbltipousuario OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16997)
-- Name: tbltokenenviocarga; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbltokenenviocarga (
    idtokenenviocarga bigint NOT NULL,
    idpatriarca bigint NOT NULL,
    idstatustokenenviocarga smallint NOT NULL,
    strtokenretorno character varying(1000) NOT NULL,
    datdatahorainicio timestamp with time zone DEFAULT now() NOT NULL,
    datdatahorafim timestamp with time zone
);


ALTER TABLE public.tbltokenenviocarga OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 16996)
-- Name: tbltokenenviocarga_idtokenenviocarga_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tbltokenenviocarga_idtokenenviocarga_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tbltokenenviocarga_idtokenenviocarga_seq OWNER TO postgres;

--
-- TOC entry 5489 (class 0 OID 0)
-- Dependencies: 228
-- Name: tbltokenenviocarga_idtokenenviocarga_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tbltokenenviocarga_idtokenenviocarga_seq OWNED BY public.tbltokenenviocarga.idtokenenviocarga;


--
-- TOC entry 223 (class 1259 OID 16901)
-- Name: tblusuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tblusuario (
    idusuario bigint NOT NULL,
    strnome character varying(200) NOT NULL,
    stremail character varying(200) NOT NULL,
    strsenha character varying(200) NOT NULL,
    idstatususuario smallint NOT NULL,
    idtipousuario smallint NOT NULL,
    idclassificacaousuario smallint NOT NULL,
    datacriacao timestamp with time zone DEFAULT now() CONSTRAINT tblusuario_data_criacao_not_null NOT NULL,
    idusuariocriacao bigint,
    data_alteracao timestamp with time zone,
    idusuarioalteracao bigint,
    is_active boolean DEFAULT true NOT NULL,
    is_staff boolean DEFAULT false NOT NULL,
    is_superuser boolean DEFAULT false NOT NULL,
    last_login timestamp with time zone,
    date_joined timestamp with time zone DEFAULT now()
);


ALTER TABLE public.tblusuario OWNER TO postgres;

--
-- TOC entry 275 (class 1259 OID 17993)
-- Name: tblusuario_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tblusuario_groups (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.tblusuario_groups OWNER TO postgres;

--
-- TOC entry 274 (class 1259 OID 17992)
-- Name: tblusuario_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tblusuario_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tblusuario_groups_id_seq OWNER TO postgres;

--
-- TOC entry 5490 (class 0 OID 0)
-- Dependencies: 274
-- Name: tblusuario_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tblusuario_groups_id_seq OWNED BY public.tblusuario_groups.id;


--
-- TOC entry 222 (class 1259 OID 16900)
-- Name: tblusuario_idusuario_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tblusuario_idusuario_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tblusuario_idusuario_seq OWNER TO postgres;

--
-- TOC entry 5491 (class 0 OID 0)
-- Dependencies: 222
-- Name: tblusuario_idusuario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tblusuario_idusuario_seq OWNED BY public.tblusuario.idusuario;


--
-- TOC entry 277 (class 1259 OID 18015)
-- Name: tblusuario_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tblusuario_user_permissions (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.tblusuario_user_permissions OWNER TO postgres;

--
-- TOC entry 276 (class 1259 OID 18014)
-- Name: tblusuario_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tblusuario_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tblusuario_user_permissions_id_seq OWNER TO postgres;

--
-- TOC entry 5492 (class 0 OID 0)
-- Dependencies: 276
-- Name: tblusuario_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tblusuario_user_permissions_id_seq OWNED BY public.tblusuario_user_permissions.id;


--
-- TOC entry 5066 (class 2604 OID 17741)
-- Name: tblaplicacao idaplicacao; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblaplicacao ALTER COLUMN idaplicacao SET DEFAULT nextval('public.tblaplicacao_idapplication_seq'::regclass);


--
-- TOC entry 5042 (class 2604 OID 17041)
-- Name: tblcargapatriarca idcargapatriarca; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblcargapatriarca ALTER COLUMN idcargapatriarca SET DEFAULT nextval('public.tblcargapatriarca_idcargapatriarca_seq'::regclass);


--
-- TOC entry 5044 (class 2604 OID 17078)
-- Name: tbldetalhestatuscarga iddetalhestatuscarga; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbldetalhestatuscarga ALTER COLUMN iddetalhestatuscarga SET DEFAULT nextval('public.tbldetalhestatuscarga_iddetalhestatuscarga_seq'::regclass);


--
-- TOC entry 5059 (class 2604 OID 17226)
-- Name: tbllotacao idlotacao; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbllotacao ALTER COLUMN idlotacao SET DEFAULT nextval('public.tbllotacao_idlotacao_seq'::regclass);


--
-- TOC entry 5064 (class 2604 OID 17323)
-- Name: tbllotacaoinconsistencia idinconsistencia; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbllotacaoinconsistencia ALTER COLUMN idinconsistencia SET DEFAULT nextval('public.tbllotacaoinconsistencia_idinconsistencia_seq'::regclass);


--
-- TOC entry 5062 (class 2604 OID 17283)
-- Name: tbllotacaojsonorgao idlotacaojsonorgao; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbllotacaojsonorgao ALTER COLUMN idlotacaojsonorgao SET DEFAULT nextval('public.tbllotacaojsonorgao_idlotacaojsonorgao_seq'::regclass);


--
-- TOC entry 5055 (class 2604 OID 17195)
-- Name: tbllotacaoversao idlotacaoversao; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbllotacaoversao ALTER COLUMN idlotacaoversao SET DEFAULT nextval('public.tbllotacaoversao_idlotacaoversao_seq'::regclass);


--
-- TOC entry 5053 (class 2604 OID 17175)
-- Name: tblorganogramajson idorganogramajson; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblorganogramajson ALTER COLUMN idorganogramajson SET DEFAULT nextval('public.tblorganogramajson_idorganogramajson_seq'::regclass);


--
-- TOC entry 5046 (class 2604 OID 17105)
-- Name: tblorganogramaversao idorganogramaversao; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblorganogramaversao ALTER COLUMN idorganogramaversao SET DEFAULT nextval('public.tblorganogramaversao_idorganogramaversao_seq'::regclass);


--
-- TOC entry 5050 (class 2604 OID 17129)
-- Name: tblorgaounidade idorgaounidade; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblorgaounidade ALTER COLUMN idorgaounidade SET DEFAULT nextval('public.tblorgaounidade_idorgaounidade_seq'::regclass);


--
-- TOC entry 5038 (class 2604 OID 16956)
-- Name: tblpatriarca idpatriarca; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblpatriarca ALTER COLUMN idpatriarca SET DEFAULT nextval('public.tblpatriarca_idpatriarca_seq'::regclass);


--
-- TOC entry 5040 (class 2604 OID 17000)
-- Name: tbltokenenviocarga idtokenenviocarga; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbltokenenviocarga ALTER COLUMN idtokenenviocarga SET DEFAULT nextval('public.tbltokenenviocarga_idtokenenviocarga_seq'::regclass);


--
-- TOC entry 5032 (class 2604 OID 16904)
-- Name: tblusuario idusuario; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario ALTER COLUMN idusuario SET DEFAULT nextval('public.tblusuario_idusuario_seq'::regclass);


--
-- TOC entry 5067 (class 2604 OID 17996)
-- Name: tblusuario_groups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario_groups ALTER COLUMN id SET DEFAULT nextval('public.tblusuario_groups_id_seq'::regclass);


--
-- TOC entry 5068 (class 2604 OID 18018)
-- Name: tblusuario_user_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.tblusuario_user_permissions_id_seq'::regclass);


--
-- TOC entry 5460 (class 0 OID 17854)
-- Dependencies: 265
-- Data for Name: accounts_attribute; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts_attribute (id, key, value, aplicacao_id, user_id) FROM stdin;
\.


--
-- TOC entry 5458 (class 0 OID 17844)
-- Dependencies: 263
-- Data for Name: accounts_role; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts_role (id, nomeperfil, codigoperfil, aplicacao_id) FROM stdin;
\.


--
-- TOC entry 5462 (class 0 OID 17864)
-- Dependencies: 267
-- Data for Name: accounts_userrole; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts_userrole (id, aplicacao_id, role_id, user_id) FROM stdin;
\.


--
-- TOC entry 5454 (class 0 OID 17795)
-- Dependencies: 259
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- TOC entry 5456 (class 0 OID 17805)
-- Dependencies: 261
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- TOC entry 5452 (class 0 OID 17785)
-- Dependencies: 257
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	3	add_permission
6	Can change permission	3	change_permission
7	Can delete permission	3	delete_permission
8	Can view permission	3	view_permission
9	Can add group	2	add_group
10	Can change group	2	change_group
11	Can delete group	2	delete_group
12	Can view group	2	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add Token	6	add_token
22	Can change Token	6	change_token
23	Can delete Token	6	delete_token
24	Can view Token	6	view_token
25	Can add Token	7	add_tokenproxy
26	Can change Token	7	change_tokenproxy
27	Can delete Token	7	delete_tokenproxy
28	Can view Token	7	view_tokenproxy
29	Can add user	11	add_user
30	Can change user	11	change_user
31	Can delete user	11	delete_user
32	Can view user	11	view_user
33	Can add aplicacao	8	add_aplicacao
34	Can change aplicacao	8	change_aplicacao
35	Can delete aplicacao	8	delete_aplicacao
36	Can view aplicacao	8	view_aplicacao
37	Can add role	10	add_role
38	Can change role	10	change_role
39	Can delete role	10	delete_role
40	Can view role	10	view_role
41	Can add attribute	9	add_attribute
42	Can change attribute	9	change_attribute
43	Can delete attribute	9	delete_attribute
44	Can view attribute	9	view_attribute
45	Can add user role	12	add_userrole
46	Can change user role	12	change_userrole
47	Can delete user role	12	delete_userrole
48	Can view user role	12	view_userrole
49	Can add app client	13	add_appclient
50	Can change app client	13	change_appclient
51	Can delete app client	13	delete_appclient
52	Can view app client	13	view_appclient
\.


--
-- TOC entry 5465 (class 0 OID 17942)
-- Dependencies: 270
-- Data for Name: authtoken_token; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.authtoken_token (key, created, user_id) FROM stdin;
\.


--
-- TOC entry 5467 (class 0 OID 17959)
-- Dependencies: 272
-- Data for Name: db_service_appclient; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.db_service_appclient (id, client_id, client_secret_hash, is_active, aplicacao_id) FROM stdin;
\.


--
-- TOC entry 5464 (class 0 OID 17916)
-- Dependencies: 269
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2026-01-13 11:45:41.801391-03	5	alexandre.mohamad@seger.es.gov.br	1	[{"added": {}}]	11	4
2	2026-01-13 11:53:18.133681-03	1	PortalGPP - Portal GPP	1	[{"added": {}}]	8	4
3	2026-01-13 11:53:51.910954-03	2	CargaUnicaOrganogramaLotacao - Carga Única de Organograma e Lotação	1	[{"added": {}}]	8	4
\.


--
-- TOC entry 5450 (class 0 OID 17773)
-- Dependencies: 255
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	group
3	auth	permission
4	contenttypes	contenttype
5	sessions	session
6	authtoken	token
7	authtoken	tokenproxy
8	accounts	aplicacao
9	accounts	attribute
10	accounts	role
11	accounts	user
12	accounts	userrole
13	db_service	appclient
\.


--
-- TOC entry 5448 (class 0 OID 17761)
-- Dependencies: 253
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2026-01-13 11:00:08.544855-03
2	contenttypes	0002_remove_content_type_name	2026-01-13 11:00:08.550002-03
3	auth	0001_initial	2026-01-13 11:00:08.574044-03
4	auth	0002_alter_permission_name_max_length	2026-01-13 11:00:08.577693-03
5	auth	0003_alter_user_email_max_length	2026-01-13 11:00:08.580238-03
6	auth	0004_alter_user_username_opts	2026-01-13 11:00:08.5832-03
7	auth	0005_alter_user_last_login_null	2026-01-13 11:00:08.5859-03
8	auth	0006_require_contenttypes_0002	2026-01-13 11:00:08.587015-03
9	auth	0007_alter_validators_add_error_messages	2026-01-13 11:00:08.589728-03
10	auth	0008_alter_user_username_max_length	2026-01-13 11:00:08.592744-03
11	auth	0009_alter_user_last_name_max_length	2026-01-13 11:00:08.595352-03
12	auth	0010_alter_group_name_max_length	2026-01-13 11:00:08.600112-03
13	auth	0011_update_proxy_permissions	2026-01-13 11:00:08.60298-03
14	auth	0012_alter_user_first_name_max_length	2026-01-13 11:00:08.606178-03
15	accounts	0001_initial	2026-01-13 11:06:59.898181-03
16	admin	0001_initial	2026-01-13 11:06:59.909921-03
17	admin	0002_logentry_remove_auto_add	2026-01-13 11:06:59.913567-03
18	admin	0003_logentry_add_action_flag_choices	2026-01-13 11:06:59.916933-03
19	authtoken	0001_initial	2026-01-13 11:06:59.928028-03
20	authtoken	0002_auto_20160226_1747	2026-01-13 11:06:59.937771-03
21	authtoken	0003_tokenproxy	2026-01-13 11:06:59.94-03
22	authtoken	0004_alter_tokenproxy_options	2026-01-13 11:06:59.941605-03
23	db_service	0001_initial	2026-01-13 11:06:59.953585-03
24	sessions	0001_initial	2026-01-13 11:06:59.960901-03
\.


--
-- TOC entry 5468 (class 0 OID 17979)
-- Dependencies: 273
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
uz2dqufjgu88n15xoktlp1wfwqdps9om	.eJxVjEEOwiAQAP_C2RAQti0evfsGsssuUjUlKe3J-HdD0oNeZybzVhH3rcS9yRpnVhfl1emXEaanLF3wA5d71aku2zqT7ok-bNO3yvK6Hu3foGArfct2mBCZLBEMWczIGOCcEriMwY3OesvgxAgFNpwdA2SPZNiDmTKpzxcCtDix:1vffHj:9ryPmv1lcL0i7Nn7HVInnos94B00jDSe-s_3UUXANV4	2026-01-27 11:22:15.924869-03
\.


--
-- TOC entry 5446 (class 0 OID 17738)
-- Dependencies: 251
-- Data for Name: tblaplicacao; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tblaplicacao (idaplicacao, codigointerno, nomeaplicacao, base_url) FROM stdin;
1	PortalGPP	Portal GPP	\N
2	CargaUnicaOrganogramaLotacao	Carga Única de Organograma e Lotação	\N
\.


--
-- TOC entry 5428 (class 0 OID 17038)
-- Dependencies: 233
-- Data for Name: tblcargapatriarca; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tblcargapatriarca (idcargapatriarca, idpatriarca, idtokenenviocarga, idstatuscarga, idtipocarga, strmensagemretorno, datdatahorainicio, datdatahorafim) FROM stdin;
\.


--
-- TOC entry 5416 (class 0 OID 16893)
-- Dependencies: 221
-- Data for Name: tblclassificacaousuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tblclassificacaousuario (idclassificacaousuario, strdescricao) FROM stdin;
1	Gestor Portal
2	Gestor Aplicação
3	Usuário Nível Básico
4	Usuário Nível Intermediário
5	Usuário Nível Avançado
\.


--
-- TOC entry 5430 (class 0 OID 17075)
-- Dependencies: 235
-- Data for Name: tbldetalhestatuscarga; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbldetalhestatuscarga (iddetalhestatuscarga, idcargapatriarca, idstatuscarga, datregistro, strmensagem) FROM stdin;
\.


--
-- TOC entry 5440 (class 0 OID 17223)
-- Dependencies: 245
-- Data for Name: tbllotacao; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbllotacao (idlotacao, idlotacaoversao, idorganogramaversao, idpatriarca, idorgaolotacao, idunidadelotacao, strcpf, strcargooriginal, strcargonormalizado, flgvalido, strerrosvalidacao, datreferencia, datcriacao, idusuariocriacao, datalteracao, idusuarioalteracao) FROM stdin;
\.


--
-- TOC entry 5444 (class 0 OID 17320)
-- Dependencies: 249
-- Data for Name: tbllotacaoinconsistencia; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbllotacaoinconsistencia (idinconsistencia, idlotacao, strtipo, strdetalhe, datregistro) FROM stdin;
\.


--
-- TOC entry 5442 (class 0 OID 17280)
-- Dependencies: 247
-- Data for Name: tbllotacaojsonorgao; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbllotacaojsonorgao (idlotacaojsonorgao, idlotacaoversao, idorganogramaversao, idpatriarca, idorgaolotacao, jsconteudo, datcriacao, datenvioapi, strstatusenvio, strmensagemretorno) FROM stdin;
\.


--
-- TOC entry 5438 (class 0 OID 17192)
-- Dependencies: 243
-- Data for Name: tbllotacaoversao; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbllotacaoversao (idlotacaoversao, idpatriarca, idorganogramaversao, strorigem, strtipoarquivooriginal, strnomearquivooriginal, datprocessamento, strstatusprocessamento, strmensagemprocessamento, flgativo) FROM stdin;
\.


--
-- TOC entry 5436 (class 0 OID 17172)
-- Dependencies: 241
-- Data for Name: tblorganogramajson; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tblorganogramajson (idorganogramajson, idorganogramaversao, jsconteudo, datcriacao, datenvioapi, strstatusenvio, strmensagemretorno) FROM stdin;
\.


--
-- TOC entry 5432 (class 0 OID 17102)
-- Dependencies: 237
-- Data for Name: tblorganogramaversao; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tblorganogramaversao (idorganogramaversao, idpatriarca, strorigem, strtipoarquivooriginal, strnomearquivooriginal, datprocessamento, strstatusprocessamento, strmensagemprocessamento, flgativo) FROM stdin;
\.


--
-- TOC entry 5434 (class 0 OID 17126)
-- Dependencies: 239
-- Data for Name: tblorgaounidade; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tblorgaounidade (idorgaounidade, idorganogramaversao, idpatriarca, strnome, strsigla, idorgaounidadepai, strnumerohierarquia, intnivelhierarquia, flgativo, datcriacao, idusuariocriacao, datalteracao, idusuarioalteracao) FROM stdin;
\.


--
-- TOC entry 5421 (class 0 OID 16953)
-- Dependencies: 226
-- Data for Name: tblpatriarca; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tblpatriarca (idpatriarca, idexternopatriarca, strsiglapatriarca, strnome, idstatusprogresso, datcriacao, idusuariocriacao, datalteracao, idusuarioalteracao) FROM stdin;
\.


--
-- TOC entry 5426 (class 0 OID 17029)
-- Dependencies: 231
-- Data for Name: tblstatuscarga; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tblstatuscarga (idstatuscarga, strdescricao, flgsucesso) FROM stdin;
1	Enviando Carga de Organograma	0
2	Organograma Enviado com sucesso	1
3	Organograma Enviado com Erro	2
4	Tempo Resposta Organograma Esgotado	2
5	Enviando Carga de Lotação	0
6	Lotação Enviada com sucesso	1
7	Lotação Enviada com Erro	2
8	Tempo Resposta Lotação Esgotado	2
9	Enviando Carga de Lotação (Arq. Único)	0
10	Lotação (Arq. Único) Enviada com sucesso	1
11	Lotação (Arq. Único) Enviada com Erro	2
12	Tempo Resposta Lotação (Arq. Único) Esgotado	2
\.


--
-- TOC entry 5419 (class 0 OID 16945)
-- Dependencies: 224
-- Data for Name: tblstatusprogresso; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tblstatusprogresso (idstatusprogresso, strdescricao) FROM stdin;
1	Nova Carga
2	Organograma em Progresso
3	Lotação em Progresso
4	Pronto para Carga
5	Carga em Processamento
6	Carga Finalizada
\.


--
-- TOC entry 5422 (class 0 OID 16989)
-- Dependencies: 227
-- Data for Name: tblstatustokenenviocarga; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tblstatustokenenviocarga (idstatustokenenviocarga, strdescricao) FROM stdin;
1	Solicitando Token
2	Token Adquirido
3	Token Negado
4	Token Expirado
5	Token Inválido
6	Tempo Ultrapassado (Solicitação)
\.


--
-- TOC entry 5414 (class 0 OID 16879)
-- Dependencies: 219
-- Data for Name: tblstatususuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tblstatususuario (idstatususuario, strdescricao) FROM stdin;
1	Ativo
2	Inativo
3	Necessita Validação
\.


--
-- TOC entry 5425 (class 0 OID 17022)
-- Dependencies: 230
-- Data for Name: tbltipocarga; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbltipocarga (idtipocarga, strdescricao) FROM stdin;
1	Organograma
2	Lotação
3	Lotação Arq. Único
\.


--
-- TOC entry 5415 (class 0 OID 16886)
-- Dependencies: 220
-- Data for Name: tbltipousuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbltipousuario (idtipousuario, strdescricao) FROM stdin;
1	Interno
2	Externo
\.


--
-- TOC entry 5424 (class 0 OID 16997)
-- Dependencies: 229
-- Data for Name: tbltokenenviocarga; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tbltokenenviocarga (idtokenenviocarga, idpatriarca, idstatustokenenviocarga, strtokenretorno, datdatahorainicio, datdatahorafim) FROM stdin;
\.


--
-- TOC entry 5418 (class 0 OID 16901)
-- Dependencies: 223
-- Data for Name: tblusuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tblusuario (idusuario, strnome, stremail, strsenha, idstatususuario, idtipousuario, idclassificacaousuario, datacriacao, idusuariocriacao, data_alteracao, idusuarioalteracao, is_active, is_staff, is_superuser, last_login, date_joined) FROM stdin;
4		acoesgpp@seger.es.gov.br	pbkdf2_sha256$1200000$W2Y60oVRgqbaKbKAHgV9gy$UOa1xOHfLuLvpiAvIv8IWx/zzKPWEzKBXd2wKuqObuY=	1	1	1	2026-01-13 11:21:35.417706-03	\N	\N	\N	t	t	t	2026-01-13 11:22:15.922483-03	\N
5	Alexandre Wanick Mohamad	alexandre.mohamad@seger.es.gov.br	pbkdf2_sha256$1200000$7T6S056t0uJiM4yA96hRV8$xvB2YWQMEMgGrkA/C8Qe9FxyIvk5JadphpahMKmbjm8=	1	1	1	2026-01-13 11:45:41.338314-03	\N	\N	\N	t	t	f	\N	\N
\.


--
-- TOC entry 5470 (class 0 OID 17993)
-- Dependencies: 275
-- Data for Name: tblusuario_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tblusuario_groups (id, user_id, group_id) FROM stdin;
\.


--
-- TOC entry 5472 (class 0 OID 18015)
-- Dependencies: 277
-- Data for Name: tblusuario_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tblusuario_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- TOC entry 5493 (class 0 OID 0)
-- Dependencies: 264
-- Name: accounts_attribute_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_attribute_id_seq', 1, false);


--
-- TOC entry 5494 (class 0 OID 0)
-- Dependencies: 262
-- Name: accounts_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_role_id_seq', 1, false);


--
-- TOC entry 5495 (class 0 OID 0)
-- Dependencies: 266
-- Name: accounts_userrole_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_userrole_id_seq', 1, false);


--
-- TOC entry 5496 (class 0 OID 0)
-- Dependencies: 258
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- TOC entry 5497 (class 0 OID 0)
-- Dependencies: 260
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- TOC entry 5498 (class 0 OID 0)
-- Dependencies: 256
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 52, true);


--
-- TOC entry 5499 (class 0 OID 0)
-- Dependencies: 271
-- Name: db_service_appclient_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.db_service_appclient_id_seq', 1, false);


--
-- TOC entry 5500 (class 0 OID 0)
-- Dependencies: 268
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 3, true);


--
-- TOC entry 5501 (class 0 OID 0)
-- Dependencies: 254
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 13, true);


--
-- TOC entry 5502 (class 0 OID 0)
-- Dependencies: 252
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 24, true);


--
-- TOC entry 5503 (class 0 OID 0)
-- Dependencies: 250
-- Name: tblaplicacao_idapplication_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tblaplicacao_idapplication_seq', 2, true);


--
-- TOC entry 5504 (class 0 OID 0)
-- Dependencies: 232
-- Name: tblcargapatriarca_idcargapatriarca_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tblcargapatriarca_idcargapatriarca_seq', 1, false);


--
-- TOC entry 5505 (class 0 OID 0)
-- Dependencies: 234
-- Name: tbldetalhestatuscarga_iddetalhestatuscarga_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tbldetalhestatuscarga_iddetalhestatuscarga_seq', 1, false);


--
-- TOC entry 5506 (class 0 OID 0)
-- Dependencies: 244
-- Name: tbllotacao_idlotacao_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tbllotacao_idlotacao_seq', 1, false);


--
-- TOC entry 5507 (class 0 OID 0)
-- Dependencies: 248
-- Name: tbllotacaoinconsistencia_idinconsistencia_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tbllotacaoinconsistencia_idinconsistencia_seq', 1, false);


--
-- TOC entry 5508 (class 0 OID 0)
-- Dependencies: 246
-- Name: tbllotacaojsonorgao_idlotacaojsonorgao_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tbllotacaojsonorgao_idlotacaojsonorgao_seq', 1, false);


--
-- TOC entry 5509 (class 0 OID 0)
-- Dependencies: 242
-- Name: tbllotacaoversao_idlotacaoversao_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tbllotacaoversao_idlotacaoversao_seq', 1, false);


--
-- TOC entry 5510 (class 0 OID 0)
-- Dependencies: 240
-- Name: tblorganogramajson_idorganogramajson_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tblorganogramajson_idorganogramajson_seq', 1, false);


--
-- TOC entry 5511 (class 0 OID 0)
-- Dependencies: 236
-- Name: tblorganogramaversao_idorganogramaversao_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tblorganogramaversao_idorganogramaversao_seq', 1, false);


--
-- TOC entry 5512 (class 0 OID 0)
-- Dependencies: 238
-- Name: tblorgaounidade_idorgaounidade_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tblorgaounidade_idorgaounidade_seq', 1, false);


--
-- TOC entry 5513 (class 0 OID 0)
-- Dependencies: 225
-- Name: tblpatriarca_idpatriarca_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tblpatriarca_idpatriarca_seq', 1, false);


--
-- TOC entry 5514 (class 0 OID 0)
-- Dependencies: 228
-- Name: tbltokenenviocarga_idtokenenviocarga_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tbltokenenviocarga_idtokenenviocarga_seq', 1, false);


--
-- TOC entry 5515 (class 0 OID 0)
-- Dependencies: 274
-- Name: tblusuario_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tblusuario_groups_id_seq', 1, false);


--
-- TOC entry 5516 (class 0 OID 0)
-- Dependencies: 222
-- Name: tblusuario_idusuario_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tblusuario_idusuario_seq', 5, true);


--
-- TOC entry 5517 (class 0 OID 0)
-- Dependencies: 276
-- Name: tblusuario_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tblusuario_user_permissions_id_seq', 1, false);


--
-- TOC entry 5170 (class 2606 OID 17862)
-- Name: accounts_attribute accounts_attribute_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_attribute
    ADD CONSTRAINT accounts_attribute_pkey PRIMARY KEY (id);


--
-- TOC entry 5172 (class 2606 OID 17882)
-- Name: accounts_attribute accounts_attribute_user_id_aplicacao_id_key_67c2d83c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_attribute
    ADD CONSTRAINT accounts_attribute_user_id_aplicacao_id_key_67c2d83c_uniq UNIQUE (user_id, aplicacao_id, key);


--
-- TOC entry 5165 (class 2606 OID 17874)
-- Name: accounts_role accounts_role_aplicacao_id_codigoperfil_474ffdb6_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_role
    ADD CONSTRAINT accounts_role_aplicacao_id_codigoperfil_474ffdb6_uniq UNIQUE (aplicacao_id, codigoperfil);


--
-- TOC entry 5167 (class 2606 OID 17852)
-- Name: accounts_role accounts_role_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_role
    ADD CONSTRAINT accounts_role_pkey PRIMARY KEY (id);


--
-- TOC entry 5176 (class 2606 OID 17872)
-- Name: accounts_userrole accounts_userrole_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_userrole
    ADD CONSTRAINT accounts_userrole_pkey PRIMARY KEY (id);


--
-- TOC entry 5179 (class 2606 OID 17896)
-- Name: accounts_userrole accounts_userrole_user_id_aplicacao_id_role_id_26c338bf_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_userrole
    ADD CONSTRAINT accounts_userrole_user_id_aplicacao_id_role_id_26c338bf_uniq UNIQUE (user_id, aplicacao_id, role_id);


--
-- TOC entry 5154 (class 2606 OID 17838)
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- TOC entry 5159 (class 2606 OID 17823)
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- TOC entry 5162 (class 2606 OID 17812)
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 5156 (class 2606 OID 17801)
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- TOC entry 5149 (class 2606 OID 17814)
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- TOC entry 5151 (class 2606 OID 17793)
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- TOC entry 5187 (class 2606 OID 17949)
-- Name: authtoken_token authtoken_token_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_pkey PRIMARY KEY (key);


--
-- TOC entry 5189 (class 2606 OID 17951)
-- Name: authtoken_token authtoken_token_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_key UNIQUE (user_id);


--
-- TOC entry 5191 (class 2606 OID 17972)
-- Name: db_service_appclient db_service_appclient_aplicacao_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.db_service_appclient
    ADD CONSTRAINT db_service_appclient_aplicacao_id_key UNIQUE (aplicacao_id);


--
-- TOC entry 5194 (class 2606 OID 17970)
-- Name: db_service_appclient db_service_appclient_client_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.db_service_appclient
    ADD CONSTRAINT db_service_appclient_client_id_key UNIQUE (client_id);


--
-- TOC entry 5196 (class 2606 OID 17968)
-- Name: db_service_appclient db_service_appclient_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.db_service_appclient
    ADD CONSTRAINT db_service_appclient_pkey PRIMARY KEY (id);


--
-- TOC entry 5183 (class 2606 OID 17929)
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- TOC entry 5144 (class 2606 OID 17783)
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- TOC entry 5146 (class 2606 OID 17781)
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- TOC entry 5142 (class 2606 OID 17771)
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- TOC entry 5199 (class 2606 OID 17988)
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- TOC entry 5138 (class 2606 OID 17750)
-- Name: tblaplicacao tblaplicacao_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblaplicacao
    ADD CONSTRAINT tblaplicacao_code_key UNIQUE (codigointerno);


--
-- TOC entry 5140 (class 2606 OID 17748)
-- Name: tblaplicacao tblaplicacao_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblaplicacao
    ADD CONSTRAINT tblaplicacao_pkey PRIMARY KEY (idaplicacao);


--
-- TOC entry 5101 (class 2606 OID 17052)
-- Name: tblcargapatriarca tblcargapatriarca_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblcargapatriarca
    ADD CONSTRAINT tblcargapatriarca_pkey PRIMARY KEY (idcargapatriarca);


--
-- TOC entry 5075 (class 2606 OID 16899)
-- Name: tblclassificacaousuario tblclassificacaousuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblclassificacaousuario
    ADD CONSTRAINT tblclassificacaousuario_pkey PRIMARY KEY (idclassificacaousuario);


--
-- TOC entry 5107 (class 2606 OID 17087)
-- Name: tbldetalhestatuscarga tbldetalhestatuscarga_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbldetalhestatuscarga
    ADD CONSTRAINT tbldetalhestatuscarga_pkey PRIMARY KEY (iddetalhestatuscarga);


--
-- TOC entry 5129 (class 2606 OID 17240)
-- Name: tbllotacao tbllotacao_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbllotacao
    ADD CONSTRAINT tbllotacao_pkey PRIMARY KEY (idlotacao);


--
-- TOC entry 5136 (class 2606 OID 17333)
-- Name: tbllotacaoinconsistencia tbllotacaoinconsistencia_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbllotacaoinconsistencia
    ADD CONSTRAINT tbllotacaoinconsistencia_pkey PRIMARY KEY (idinconsistencia);


--
-- TOC entry 5132 (class 2606 OID 17295)
-- Name: tbllotacaojsonorgao tbllotacaojsonorgao_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbllotacaojsonorgao
    ADD CONSTRAINT tbllotacaojsonorgao_pkey PRIMARY KEY (idlotacaojsonorgao);


--
-- TOC entry 5124 (class 2606 OID 17209)
-- Name: tbllotacaoversao tbllotacaoversao_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbllotacaoversao
    ADD CONSTRAINT tbllotacaoversao_pkey PRIMARY KEY (idlotacaoversao);


--
-- TOC entry 5119 (class 2606 OID 17184)
-- Name: tblorganogramajson tblorganogramajson_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblorganogramajson
    ADD CONSTRAINT tblorganogramajson_pkey PRIMARY KEY (idorganogramajson);


--
-- TOC entry 5110 (class 2606 OID 17118)
-- Name: tblorganogramaversao tblorganogramaversao_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblorganogramaversao
    ADD CONSTRAINT tblorganogramaversao_pkey PRIMARY KEY (idorganogramaversao);


--
-- TOC entry 5115 (class 2606 OID 17140)
-- Name: tblorgaounidade tblorgaounidade_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblorgaounidade
    ADD CONSTRAINT tblorgaounidade_pkey PRIMARY KEY (idorgaounidade);


--
-- TOC entry 5086 (class 2606 OID 16966)
-- Name: tblpatriarca tblpatriarca_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblpatriarca
    ADD CONSTRAINT tblpatriarca_pkey PRIMARY KEY (idpatriarca);


--
-- TOC entry 5099 (class 2606 OID 17036)
-- Name: tblstatuscarga tblstatuscarga_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblstatuscarga
    ADD CONSTRAINT tblstatuscarga_pkey PRIMARY KEY (idstatuscarga);


--
-- TOC entry 5081 (class 2606 OID 16951)
-- Name: tblstatusprogresso tblstatusprogresso_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblstatusprogresso
    ADD CONSTRAINT tblstatusprogresso_pkey PRIMARY KEY (idstatusprogresso);


--
-- TOC entry 5092 (class 2606 OID 16995)
-- Name: tblstatustokenenviocarga tblstatustokenenviocarga_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblstatustokenenviocarga
    ADD CONSTRAINT tblstatustokenenviocarga_pkey PRIMARY KEY (idstatustokenenviocarga);


--
-- TOC entry 5071 (class 2606 OID 16885)
-- Name: tblstatususuario tblstatususuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblstatususuario
    ADD CONSTRAINT tblstatususuario_pkey PRIMARY KEY (idstatususuario);


--
-- TOC entry 5097 (class 2606 OID 17028)
-- Name: tbltipocarga tbltipocarga_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbltipocarga
    ADD CONSTRAINT tbltipocarga_pkey PRIMARY KEY (idtipocarga);


--
-- TOC entry 5073 (class 2606 OID 16892)
-- Name: tbltipousuario tbltipousuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbltipousuario
    ADD CONSTRAINT tbltipousuario_pkey PRIMARY KEY (idtipousuario);


--
-- TOC entry 5095 (class 2606 OID 17010)
-- Name: tbltokenenviocarga tbltokenenviocarga_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbltokenenviocarga
    ADD CONSTRAINT tbltokenenviocarga_pkey PRIMARY KEY (idtokenenviocarga);


--
-- TOC entry 5204 (class 2606 OID 18001)
-- Name: tblusuario_groups tblusuario_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario_groups
    ADD CONSTRAINT tblusuario_groups_pkey PRIMARY KEY (id);


--
-- TOC entry 5206 (class 2606 OID 18003)
-- Name: tblusuario_groups tblusuario_groups_user_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario_groups
    ADD CONSTRAINT tblusuario_groups_user_id_group_id_key UNIQUE (user_id, group_id);


--
-- TOC entry 5077 (class 2606 OID 16917)
-- Name: tblusuario tblusuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario
    ADD CONSTRAINT tblusuario_pkey PRIMARY KEY (idusuario);


--
-- TOC entry 5079 (class 2606 OID 16919)
-- Name: tblusuario tblusuario_stremail_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario
    ADD CONSTRAINT tblusuario_stremail_key UNIQUE (stremail);


--
-- TOC entry 5210 (class 2606 OID 18023)
-- Name: tblusuario_user_permissions tblusuario_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario_user_permissions
    ADD CONSTRAINT tblusuario_user_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 5212 (class 2606 OID 18025)
-- Name: tblusuario_user_permissions tblusuario_user_permissions_user_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario_user_permissions
    ADD CONSTRAINT tblusuario_user_permissions_user_id_permission_id_key UNIQUE (user_id, permission_id);


--
-- TOC entry 5134 (class 2606 OID 17297)
-- Name: tbllotacaojsonorgao uq_lotjson_versao_org; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbllotacaojsonorgao
    ADD CONSTRAINT uq_lotjson_versao_org UNIQUE (idlotacaoversao, idorgaolotacao);


--
-- TOC entry 5117 (class 2606 OID 17142)
-- Name: tblorgaounidade uq_orgao_versao_sigla; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblorgaounidade
    ADD CONSTRAINT uq_orgao_versao_sigla UNIQUE (idorganogramaversao, strsigla);


--
-- TOC entry 5088 (class 2606 OID 16968)
-- Name: tblpatriarca uq_patriarca_idexterno; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblpatriarca
    ADD CONSTRAINT uq_patriarca_idexterno UNIQUE (idexternopatriarca);


--
-- TOC entry 5090 (class 2606 OID 16970)
-- Name: tblpatriarca uq_patriarca_sigla; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblpatriarca
    ADD CONSTRAINT uq_patriarca_sigla UNIQUE (strsiglapatriarca);


--
-- TOC entry 5168 (class 1259 OID 17893)
-- Name: accounts_attribute_aplicacao_id_5139e1c1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_attribute_aplicacao_id_5139e1c1 ON public.accounts_attribute USING btree (aplicacao_id);


--
-- TOC entry 5173 (class 1259 OID 17894)
-- Name: accounts_attribute_user_id_e505d190; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_attribute_user_id_e505d190 ON public.accounts_attribute USING btree (user_id);


--
-- TOC entry 5163 (class 1259 OID 17880)
-- Name: accounts_role_aplicacao_id_180a9da1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_role_aplicacao_id_180a9da1 ON public.accounts_role USING btree (aplicacao_id);


--
-- TOC entry 5174 (class 1259 OID 17912)
-- Name: accounts_userrole_aplicacao_id_e9e35b67; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_userrole_aplicacao_id_e9e35b67 ON public.accounts_userrole USING btree (aplicacao_id);


--
-- TOC entry 5177 (class 1259 OID 17913)
-- Name: accounts_userrole_role_id_9448d870; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_userrole_role_id_9448d870 ON public.accounts_userrole USING btree (role_id);


--
-- TOC entry 5180 (class 1259 OID 17914)
-- Name: accounts_userrole_user_id_eba3c754; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_userrole_user_id_eba3c754 ON public.accounts_userrole USING btree (user_id);


--
-- TOC entry 5152 (class 1259 OID 17839)
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- TOC entry 5157 (class 1259 OID 17834)
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- TOC entry 5160 (class 1259 OID 17835)
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- TOC entry 5147 (class 1259 OID 17820)
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- TOC entry 5185 (class 1259 OID 17957)
-- Name: authtoken_token_key_10f0b77e_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX authtoken_token_key_10f0b77e_like ON public.authtoken_token USING btree (key varchar_pattern_ops);


--
-- TOC entry 5192 (class 1259 OID 17978)
-- Name: db_service_appclient_client_id_a6545fb2_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX db_service_appclient_client_id_a6545fb2_like ON public.db_service_appclient USING btree (client_id varchar_pattern_ops);


--
-- TOC entry 5181 (class 1259 OID 17940)
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- TOC entry 5184 (class 1259 OID 17941)
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- TOC entry 5197 (class 1259 OID 17990)
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- TOC entry 5200 (class 1259 OID 17989)
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- TOC entry 5103 (class 1259 OID 17098)
-- Name: idx_detstatus_carga; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_detstatus_carga ON public.tbldetalhestatuscarga USING btree (idcargapatriarca);


--
-- TOC entry 5104 (class 1259 OID 17100)
-- Name: idx_detstatus_data; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_detstatus_data ON public.tbldetalhestatuscarga USING btree (datregistro);


--
-- TOC entry 5105 (class 1259 OID 17099)
-- Name: idx_detstatus_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_detstatus_status ON public.tbldetalhestatuscarga USING btree (idstatuscarga);


--
-- TOC entry 5125 (class 1259 OID 17277)
-- Name: idx_lotacao_cpf; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_lotacao_cpf ON public.tbllotacao USING btree (strcpf);


--
-- TOC entry 5126 (class 1259 OID 17278)
-- Name: idx_lotacao_org; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_lotacao_org ON public.tbllotacao USING btree (idorgaolotacao);


--
-- TOC entry 5127 (class 1259 OID 17276)
-- Name: idx_lotacao_versao; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_lotacao_versao ON public.tbllotacao USING btree (idlotacaoversao);


--
-- TOC entry 5130 (class 1259 OID 17318)
-- Name: idx_lotjson_orgversao; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_lotjson_orgversao ON public.tbllotacaojsonorgao USING btree (idorganogramaversao);


--
-- TOC entry 5121 (class 1259 OID 17221)
-- Name: idx_lotvers_orgvers; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_lotvers_orgvers ON public.tbllotacaoversao USING btree (idorganogramaversao);


--
-- TOC entry 5122 (class 1259 OID 17220)
-- Name: idx_lotvers_patriarca; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_lotvers_patriarca ON public.tbllotacaoversao USING btree (idpatriarca);


--
-- TOC entry 5111 (class 1259 OID 17170)
-- Name: idx_orgao_numero; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_orgao_numero ON public.tblorgaounidade USING btree (strnumerohierarquia);


--
-- TOC entry 5112 (class 1259 OID 17169)
-- Name: idx_orgao_pai; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_orgao_pai ON public.tblorgaounidade USING btree (idorgaounidadepai);


--
-- TOC entry 5113 (class 1259 OID 17168)
-- Name: idx_orgao_versao; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_orgao_versao ON public.tblorgaounidade USING btree (idorganogramaversao);


--
-- TOC entry 5108 (class 1259 OID 17124)
-- Name: idx_orgvers_patriarca; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_orgvers_patriarca ON public.tblorganogramaversao USING btree (idpatriarca);


--
-- TOC entry 5082 (class 1259 OID 16987)
-- Name: idx_patriarca_idexterno; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_patriarca_idexterno ON public.tblpatriarca USING btree (idexternopatriarca);


--
-- TOC entry 5083 (class 1259 OID 16986)
-- Name: idx_patriarca_nome; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_patriarca_nome ON public.tblpatriarca USING btree (strnome);


--
-- TOC entry 5084 (class 1259 OID 16988)
-- Name: idx_patriarca_sigla; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_patriarca_sigla ON public.tblpatriarca USING btree (strsiglapatriarca);


--
-- TOC entry 5201 (class 1259 OID 18037)
-- Name: idx_tblusuario_groups_group; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_tblusuario_groups_group ON public.tblusuario_groups USING btree (group_id);


--
-- TOC entry 5202 (class 1259 OID 18036)
-- Name: idx_tblusuario_groups_user; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_tblusuario_groups_user ON public.tblusuario_groups USING btree (user_id);


--
-- TOC entry 5207 (class 1259 OID 18039)
-- Name: idx_tblusuario_perms_perm; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_tblusuario_perms_perm ON public.tblusuario_user_permissions USING btree (permission_id);


--
-- TOC entry 5208 (class 1259 OID 18038)
-- Name: idx_tblusuario_perms_user; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_tblusuario_perms_user ON public.tblusuario_user_permissions USING btree (user_id);


--
-- TOC entry 5093 (class 1259 OID 17021)
-- Name: idx_token_patriarca; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_token_patriarca ON public.tbltokenenviocarga USING btree (idpatriarca);


--
-- TOC entry 5102 (class 1259 OID 17073)
-- Name: uq_carga_patriarca_token_tipo; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX uq_carga_patriarca_token_tipo ON public.tblcargapatriarca USING btree (idpatriarca, idtokenenviocarga, idtipocarga);


--
-- TOC entry 5120 (class 1259 OID 17190)
-- Name: uq_orgjson_versao; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX uq_orgjson_versao ON public.tblorganogramajson USING btree (idorganogramaversao);


--
-- TOC entry 5254 (class 2606 OID 17883)
-- Name: accounts_attribute accounts_attribute_aplicacao_id_5139e1c1_fk_tblaplica; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_attribute
    ADD CONSTRAINT accounts_attribute_aplicacao_id_5139e1c1_fk_tblaplica FOREIGN KEY (aplicacao_id) REFERENCES public.tblaplicacao(idaplicacao) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5255 (class 2606 OID 17888)
-- Name: accounts_attribute accounts_attribute_user_id_e505d190_fk_tblusuario_idusuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_attribute
    ADD CONSTRAINT accounts_attribute_user_id_e505d190_fk_tblusuario_idusuario FOREIGN KEY (user_id) REFERENCES public.tblusuario(idusuario) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5253 (class 2606 OID 17875)
-- Name: accounts_role accounts_role_aplicacao_id_180a9da1_fk_tblaplicacao_idaplicacao; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_role
    ADD CONSTRAINT accounts_role_aplicacao_id_180a9da1_fk_tblaplicacao_idaplicacao FOREIGN KEY (aplicacao_id) REFERENCES public.tblaplicacao(idaplicacao) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5256 (class 2606 OID 17897)
-- Name: accounts_userrole accounts_userrole_aplicacao_id_e9e35b67_fk_tblaplica; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_userrole
    ADD CONSTRAINT accounts_userrole_aplicacao_id_e9e35b67_fk_tblaplica FOREIGN KEY (aplicacao_id) REFERENCES public.tblaplicacao(idaplicacao) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5257 (class 2606 OID 17902)
-- Name: accounts_userrole accounts_userrole_role_id_9448d870_fk_accounts_role_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_userrole
    ADD CONSTRAINT accounts_userrole_role_id_9448d870_fk_accounts_role_id FOREIGN KEY (role_id) REFERENCES public.accounts_role(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5258 (class 2606 OID 17907)
-- Name: accounts_userrole accounts_userrole_user_id_eba3c754_fk_tblusuario_idusuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_userrole
    ADD CONSTRAINT accounts_userrole_user_id_eba3c754_fk_tblusuario_idusuario FOREIGN KEY (user_id) REFERENCES public.tblusuario(idusuario) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5251 (class 2606 OID 17829)
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5252 (class 2606 OID 17824)
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5250 (class 2606 OID 17815)
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5261 (class 2606 OID 17952)
-- Name: authtoken_token authtoken_token_user_id_35299eff_fk_tblusuario_idusuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_35299eff_fk_tblusuario_idusuario FOREIGN KEY (user_id) REFERENCES public.tblusuario(idusuario) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5262 (class 2606 OID 17973)
-- Name: db_service_appclient db_service_appclient_aplicacao_id_bd7a7a76_fk_tblaplica; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.db_service_appclient
    ADD CONSTRAINT db_service_appclient_aplicacao_id_bd7a7a76_fk_tblaplica FOREIGN KEY (aplicacao_id) REFERENCES public.tblaplicacao(idaplicacao) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5259 (class 2606 OID 17930)
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5260 (class 2606 OID 17935)
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_tblusuario_idusuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_tblusuario_idusuario FOREIGN KEY (user_id) REFERENCES public.tblusuario(idusuario) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5223 (class 2606 OID 17053)
-- Name: tblcargapatriarca tblcargapatriarca_idpatriarca_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblcargapatriarca
    ADD CONSTRAINT tblcargapatriarca_idpatriarca_fkey FOREIGN KEY (idpatriarca) REFERENCES public.tblpatriarca(idpatriarca);


--
-- TOC entry 5224 (class 2606 OID 17063)
-- Name: tblcargapatriarca tblcargapatriarca_idstatuscarga_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblcargapatriarca
    ADD CONSTRAINT tblcargapatriarca_idstatuscarga_fkey FOREIGN KEY (idstatuscarga) REFERENCES public.tblstatuscarga(idstatuscarga);


--
-- TOC entry 5225 (class 2606 OID 17068)
-- Name: tblcargapatriarca tblcargapatriarca_idtipocarga_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblcargapatriarca
    ADD CONSTRAINT tblcargapatriarca_idtipocarga_fkey FOREIGN KEY (idtipocarga) REFERENCES public.tbltipocarga(idtipocarga);


--
-- TOC entry 5226 (class 2606 OID 17058)
-- Name: tblcargapatriarca tblcargapatriarca_idtokenenviocarga_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblcargapatriarca
    ADD CONSTRAINT tblcargapatriarca_idtokenenviocarga_fkey FOREIGN KEY (idtokenenviocarga) REFERENCES public.tbltokenenviocarga(idtokenenviocarga);


--
-- TOC entry 5227 (class 2606 OID 17088)
-- Name: tbldetalhestatuscarga tbldetalhestatuscarga_idcargapatriarca_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbldetalhestatuscarga
    ADD CONSTRAINT tbldetalhestatuscarga_idcargapatriarca_fkey FOREIGN KEY (idcargapatriarca) REFERENCES public.tblcargapatriarca(idcargapatriarca) ON DELETE CASCADE;


--
-- TOC entry 5228 (class 2606 OID 17093)
-- Name: tbldetalhestatuscarga tbldetalhestatuscarga_idstatuscarga_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbldetalhestatuscarga
    ADD CONSTRAINT tbldetalhestatuscarga_idstatuscarga_fkey FOREIGN KEY (idstatuscarga) REFERENCES public.tblstatuscarga(idstatuscarga);


--
-- TOC entry 5238 (class 2606 OID 17241)
-- Name: tbllotacao tbllotacao_idlotacaoversao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbllotacao
    ADD CONSTRAINT tbllotacao_idlotacaoversao_fkey FOREIGN KEY (idlotacaoversao) REFERENCES public.tbllotacaoversao(idlotacaoversao) ON DELETE CASCADE;


--
-- TOC entry 5239 (class 2606 OID 17246)
-- Name: tbllotacao tbllotacao_idorganogramaversao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbllotacao
    ADD CONSTRAINT tbllotacao_idorganogramaversao_fkey FOREIGN KEY (idorganogramaversao) REFERENCES public.tblorganogramaversao(idorganogramaversao);


--
-- TOC entry 5240 (class 2606 OID 17256)
-- Name: tbllotacao tbllotacao_idorgaolotacao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbllotacao
    ADD CONSTRAINT tbllotacao_idorgaolotacao_fkey FOREIGN KEY (idorgaolotacao) REFERENCES public.tblorgaounidade(idorgaounidade);


--
-- TOC entry 5241 (class 2606 OID 17251)
-- Name: tbllotacao tbllotacao_idpatriarca_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbllotacao
    ADD CONSTRAINT tbllotacao_idpatriarca_fkey FOREIGN KEY (idpatriarca) REFERENCES public.tblpatriarca(idpatriarca);


--
-- TOC entry 5242 (class 2606 OID 17261)
-- Name: tbllotacao tbllotacao_idunidadelotacao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbllotacao
    ADD CONSTRAINT tbllotacao_idunidadelotacao_fkey FOREIGN KEY (idunidadelotacao) REFERENCES public.tblorgaounidade(idorgaounidade);


--
-- TOC entry 5243 (class 2606 OID 17271)
-- Name: tbllotacao tbllotacao_idusuarioalteracao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbllotacao
    ADD CONSTRAINT tbllotacao_idusuarioalteracao_fkey FOREIGN KEY (idusuarioalteracao) REFERENCES public.tblusuario(idusuario);


--
-- TOC entry 5244 (class 2606 OID 17266)
-- Name: tbllotacao tbllotacao_idusuariocriacao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbllotacao
    ADD CONSTRAINT tbllotacao_idusuariocriacao_fkey FOREIGN KEY (idusuariocriacao) REFERENCES public.tblusuario(idusuario);


--
-- TOC entry 5249 (class 2606 OID 17334)
-- Name: tbllotacaoinconsistencia tbllotacaoinconsistencia_idlotacao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbllotacaoinconsistencia
    ADD CONSTRAINT tbllotacaoinconsistencia_idlotacao_fkey FOREIGN KEY (idlotacao) REFERENCES public.tbllotacao(idlotacao) ON DELETE CASCADE;


--
-- TOC entry 5245 (class 2606 OID 17298)
-- Name: tbllotacaojsonorgao tbllotacaojsonorgao_idlotacaoversao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbllotacaojsonorgao
    ADD CONSTRAINT tbllotacaojsonorgao_idlotacaoversao_fkey FOREIGN KEY (idlotacaoversao) REFERENCES public.tbllotacaoversao(idlotacaoversao) ON DELETE CASCADE;


--
-- TOC entry 5246 (class 2606 OID 17303)
-- Name: tbllotacaojsonorgao tbllotacaojsonorgao_idorganogramaversao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbllotacaojsonorgao
    ADD CONSTRAINT tbllotacaojsonorgao_idorganogramaversao_fkey FOREIGN KEY (idorganogramaversao) REFERENCES public.tblorganogramaversao(idorganogramaversao);


--
-- TOC entry 5247 (class 2606 OID 17313)
-- Name: tbllotacaojsonorgao tbllotacaojsonorgao_idorgaolotacao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbllotacaojsonorgao
    ADD CONSTRAINT tbllotacaojsonorgao_idorgaolotacao_fkey FOREIGN KEY (idorgaolotacao) REFERENCES public.tblorgaounidade(idorgaounidade);


--
-- TOC entry 5248 (class 2606 OID 17308)
-- Name: tbllotacaojsonorgao tbllotacaojsonorgao_idpatriarca_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbllotacaojsonorgao
    ADD CONSTRAINT tbllotacaojsonorgao_idpatriarca_fkey FOREIGN KEY (idpatriarca) REFERENCES public.tblpatriarca(idpatriarca);


--
-- TOC entry 5236 (class 2606 OID 17215)
-- Name: tbllotacaoversao tbllotacaoversao_idorganogramaversao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbllotacaoversao
    ADD CONSTRAINT tbllotacaoversao_idorganogramaversao_fkey FOREIGN KEY (idorganogramaversao) REFERENCES public.tblorganogramaversao(idorganogramaversao);


--
-- TOC entry 5237 (class 2606 OID 17210)
-- Name: tbllotacaoversao tbllotacaoversao_idpatriarca_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbllotacaoversao
    ADD CONSTRAINT tbllotacaoversao_idpatriarca_fkey FOREIGN KEY (idpatriarca) REFERENCES public.tblpatriarca(idpatriarca);


--
-- TOC entry 5235 (class 2606 OID 17185)
-- Name: tblorganogramajson tblorganogramajson_idorganogramaversao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblorganogramajson
    ADD CONSTRAINT tblorganogramajson_idorganogramaversao_fkey FOREIGN KEY (idorganogramaversao) REFERENCES public.tblorganogramaversao(idorganogramaversao) ON DELETE CASCADE;


--
-- TOC entry 5229 (class 2606 OID 17119)
-- Name: tblorganogramaversao tblorganogramaversao_idpatriarca_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblorganogramaversao
    ADD CONSTRAINT tblorganogramaversao_idpatriarca_fkey FOREIGN KEY (idpatriarca) REFERENCES public.tblpatriarca(idpatriarca);


--
-- TOC entry 5230 (class 2606 OID 17143)
-- Name: tblorgaounidade tblorgaounidade_idorganogramaversao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblorgaounidade
    ADD CONSTRAINT tblorgaounidade_idorganogramaversao_fkey FOREIGN KEY (idorganogramaversao) REFERENCES public.tblorganogramaversao(idorganogramaversao) ON DELETE RESTRICT;


--
-- TOC entry 5231 (class 2606 OID 17153)
-- Name: tblorgaounidade tblorgaounidade_idorgaounidadepai_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblorgaounidade
    ADD CONSTRAINT tblorgaounidade_idorgaounidadepai_fkey FOREIGN KEY (idorgaounidadepai) REFERENCES public.tblorgaounidade(idorgaounidade);


--
-- TOC entry 5232 (class 2606 OID 17148)
-- Name: tblorgaounidade tblorgaounidade_idpatriarca_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblorgaounidade
    ADD CONSTRAINT tblorgaounidade_idpatriarca_fkey FOREIGN KEY (idpatriarca) REFERENCES public.tblpatriarca(idpatriarca) ON DELETE RESTRICT;


--
-- TOC entry 5233 (class 2606 OID 17163)
-- Name: tblorgaounidade tblorgaounidade_idusuarioalteracao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblorgaounidade
    ADD CONSTRAINT tblorgaounidade_idusuarioalteracao_fkey FOREIGN KEY (idusuarioalteracao) REFERENCES public.tblusuario(idusuario);


--
-- TOC entry 5234 (class 2606 OID 17158)
-- Name: tblorgaounidade tblorgaounidade_idusuariocriacao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblorgaounidade
    ADD CONSTRAINT tblorgaounidade_idusuariocriacao_fkey FOREIGN KEY (idusuariocriacao) REFERENCES public.tblusuario(idusuario);


--
-- TOC entry 5218 (class 2606 OID 16971)
-- Name: tblpatriarca tblpatriarca_idstatusprogresso_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblpatriarca
    ADD CONSTRAINT tblpatriarca_idstatusprogresso_fkey FOREIGN KEY (idstatusprogresso) REFERENCES public.tblstatusprogresso(idstatusprogresso);


--
-- TOC entry 5219 (class 2606 OID 16981)
-- Name: tblpatriarca tblpatriarca_idusuarioalteracao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblpatriarca
    ADD CONSTRAINT tblpatriarca_idusuarioalteracao_fkey FOREIGN KEY (idusuarioalteracao) REFERENCES public.tblusuario(idusuario);


--
-- TOC entry 5220 (class 2606 OID 16976)
-- Name: tblpatriarca tblpatriarca_idusuariocriacao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblpatriarca
    ADD CONSTRAINT tblpatriarca_idusuariocriacao_fkey FOREIGN KEY (idusuariocriacao) REFERENCES public.tblusuario(idusuario);


--
-- TOC entry 5221 (class 2606 OID 17011)
-- Name: tbltokenenviocarga tbltokenenviocarga_idpatriarca_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbltokenenviocarga
    ADD CONSTRAINT tbltokenenviocarga_idpatriarca_fkey FOREIGN KEY (idpatriarca) REFERENCES public.tblpatriarca(idpatriarca);


--
-- TOC entry 5222 (class 2606 OID 17016)
-- Name: tbltokenenviocarga tbltokenenviocarga_idstatustokenenviocarga_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbltokenenviocarga
    ADD CONSTRAINT tbltokenenviocarga_idstatustokenenviocarga_fkey FOREIGN KEY (idstatustokenenviocarga) REFERENCES public.tblstatustokenenviocarga(idstatustokenenviocarga);


--
-- TOC entry 5263 (class 2606 OID 18009)
-- Name: tblusuario_groups tblusuario_groups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario_groups
    ADD CONSTRAINT tblusuario_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.auth_group(id) ON DELETE CASCADE;


--
-- TOC entry 5264 (class 2606 OID 18004)
-- Name: tblusuario_groups tblusuario_groups_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario_groups
    ADD CONSTRAINT tblusuario_groups_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.tblusuario(idusuario) ON DELETE CASCADE;


--
-- TOC entry 5213 (class 2606 OID 16930)
-- Name: tblusuario tblusuario_idclassificacaousuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario
    ADD CONSTRAINT tblusuario_idclassificacaousuario_fkey FOREIGN KEY (idclassificacaousuario) REFERENCES public.tblclassificacaousuario(idclassificacaousuario);


--
-- TOC entry 5214 (class 2606 OID 16920)
-- Name: tblusuario tblusuario_idstatususuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario
    ADD CONSTRAINT tblusuario_idstatususuario_fkey FOREIGN KEY (idstatususuario) REFERENCES public.tblstatususuario(idstatususuario);


--
-- TOC entry 5215 (class 2606 OID 16925)
-- Name: tblusuario tblusuario_idtipousuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario
    ADD CONSTRAINT tblusuario_idtipousuario_fkey FOREIGN KEY (idtipousuario) REFERENCES public.tbltipousuario(idtipousuario);


--
-- TOC entry 5216 (class 2606 OID 16940)
-- Name: tblusuario tblusuario_idusuarioalteracao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario
    ADD CONSTRAINT tblusuario_idusuarioalteracao_fkey FOREIGN KEY (idusuarioalteracao) REFERENCES public.tblusuario(idusuario);


--
-- TOC entry 5217 (class 2606 OID 16935)
-- Name: tblusuario tblusuario_idusuariocriacao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario
    ADD CONSTRAINT tblusuario_idusuariocriacao_fkey FOREIGN KEY (idusuariocriacao) REFERENCES public.tblusuario(idusuario);


--
-- TOC entry 5265 (class 2606 OID 18031)
-- Name: tblusuario_user_permissions tblusuario_user_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario_user_permissions
    ADD CONSTRAINT tblusuario_user_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) ON DELETE CASCADE;


--
-- TOC entry 5266 (class 2606 OID 18026)
-- Name: tblusuario_user_permissions tblusuario_user_permissions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario_user_permissions
    ADD CONSTRAINT tblusuario_user_permissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.tblusuario(idusuario) ON DELETE CASCADE;


-- Completed on 2026-01-13 13:17:34

--
-- PostgreSQL database dump complete
--

\unrestrict YbeGzjdcDByvR8O2TQlOfURcKKBBoG7WzuucYr8RhT12CzqmF2R7PUn8bIKnL4L

