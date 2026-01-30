--
-- PostgreSQL database dump
--

\restrict 3hnj753vFqsx3AJikubXIr9D9e77XKYgaVbCH2uthjhYqYRPPxgA2WuQp7Eb2SH

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

-- Started on 2026-01-30 11:00:10

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
-- TOC entry 6 (class 2615 OID 18040)
-- Name: acoes_pngi; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA acoes_pngi;


ALTER SCHEMA acoes_pngi OWNER TO postgres;

--
-- TOC entry 5548 (class 0 OID 0)
-- Dependencies: 6
-- Name: SCHEMA acoes_pngi; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA acoes_pngi IS 'Schema para aplicação de Ações do PNGI (Plano Nacional de Gestão e Inovação)';


--
-- TOC entry 5 (class 2615 OID 18095)
-- Name: carga_org_lot; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA carga_org_lot;


ALTER SCHEMA carga_org_lot OWNER TO postgres;

--
-- TOC entry 288 (class 1255 OID 18131)
-- Name: acoes_pngi_create_eixo(character varying, character varying); Type: FUNCTION; Schema: acoes_pngi; Owner: postgres
--

CREATE FUNCTION acoes_pngi.acoes_pngi_create_eixo(p_alias character varying, p_descricao character varying) RETURNS integer
    LANGUAGE plpgsql SECURITY DEFINER
    AS $$
DECLARE
    new_id INTEGER;
BEGIN
    INSERT INTO acoes_pngi.tbleixo (stralias, strdescricaoeixo, created_at, updated_at)
    VALUES (p_alias, p_descricao, NOW(), NOW())
    RETURNING ideixo INTO new_id;
    RETURN new_id;
END;
$$;


ALTER FUNCTION acoes_pngi.acoes_pngi_create_eixo(p_alias character varying, p_descricao character varying) OWNER TO postgres;

--
-- TOC entry 302 (class 1255 OID 18085)
-- Name: update_updated_at_column(); Type: FUNCTION; Schema: acoes_pngi; Owner: postgres
--

CREATE FUNCTION acoes_pngi.update_updated_at_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;


ALTER FUNCTION acoes_pngi.update_updated_at_column() OWNER TO postgres;

--
-- TOC entry 306 (class 1255 OID 18111)
-- Name: sp_get_timeline_carga(bigint); Type: FUNCTION; Schema: carga_org_lot; Owner: postgres
--

CREATE FUNCTION carga_org_lot.sp_get_timeline_carga(p_idcargapatriarca bigint) RETURNS TABLE(idstatuscarga smallint, strdescricao text, datregistro timestamp with time zone, strmensagem text)
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


ALTER FUNCTION carga_org_lot.sp_get_timeline_carga(p_idcargapatriarca bigint) OWNER TO postgres;

--
-- TOC entry 307 (class 1255 OID 18103)
-- Name: sp_insert_carga_patriarca(bigint, bigint, integer, integer, text); Type: FUNCTION; Schema: carga_org_lot; Owner: postgres
--

CREATE FUNCTION carga_org_lot.sp_insert_carga_patriarca(p_idpatriarca bigint, p_idtokenenviocarga bigint, p_idstatuscarga integer, p_idtipocarga integer, p_strmensagemretorno text) RETURNS bigint
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


ALTER FUNCTION carga_org_lot.sp_insert_carga_patriarca(p_idpatriarca bigint, p_idtokenenviocarga bigint, p_idstatuscarga integer, p_idtipocarga integer, p_strmensagemretorno text) OWNER TO postgres;

--
-- TOC entry 312 (class 1255 OID 18104)
-- Name: sp_insert_detalhe_status_carga(bigint, integer, text); Type: FUNCTION; Schema: carga_org_lot; Owner: postgres
--

CREATE FUNCTION carga_org_lot.sp_insert_detalhe_status_carga(p_idcargapatriarca bigint, p_idstatuscarga integer, p_strmensagem text) RETURNS bigint
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


ALTER FUNCTION carga_org_lot.sp_insert_detalhe_status_carga(p_idcargapatriarca bigint, p_idstatuscarga integer, p_strmensagem text) OWNER TO postgres;

--
-- TOC entry 308 (class 1255 OID 18105)
-- Name: sp_insert_lotacao(bigint, bigint, bigint, bigint, text, text, text, boolean, text, date, bigint); Type: FUNCTION; Schema: carga_org_lot; Owner: postgres
--

CREATE FUNCTION carga_org_lot.sp_insert_lotacao(p_idlotacaoversao bigint, p_idpatriarca bigint, p_idorgaolotacao bigint, p_idunidadelotacao bigint, p_strcpf text, p_strcargooriginal text, p_strcargonormalizado text, p_flgvalido boolean, p_strerrosvalidacao text, p_datreferencia date, p_idusuariocriacao bigint) RETURNS bigint
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


ALTER FUNCTION carga_org_lot.sp_insert_lotacao(p_idlotacaoversao bigint, p_idpatriarca bigint, p_idorgaolotacao bigint, p_idunidadelotacao bigint, p_strcpf text, p_strcargooriginal text, p_strcargonormalizado text, p_flgvalido boolean, p_strerrosvalidacao text, p_datreferencia date, p_idusuariocriacao bigint) OWNER TO postgres;

--
-- TOC entry 313 (class 1255 OID 18106)
-- Name: sp_insert_lotacao_inconsistencia(bigint, text, text); Type: FUNCTION; Schema: carga_org_lot; Owner: postgres
--

CREATE FUNCTION carga_org_lot.sp_insert_lotacao_inconsistencia(p_idlotacao bigint, p_strtipo text, p_strdetalhe text) RETURNS bigint
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


ALTER FUNCTION carga_org_lot.sp_insert_lotacao_inconsistencia(p_idlotacao bigint, p_strtipo text, p_strdetalhe text) OWNER TO postgres;

--
-- TOC entry 309 (class 1255 OID 18107)
-- Name: sp_insert_lotacao_json_orgao(bigint, bigint, bigint, bigint, jsonb); Type: FUNCTION; Schema: carga_org_lot; Owner: postgres
--

CREATE FUNCTION carga_org_lot.sp_insert_lotacao_json_orgao(p_idlotacaoversao bigint, p_idorganogramaversao bigint, p_idpatriarca bigint, p_idorgaolotacao bigint, p_jsconteudo jsonb) RETURNS bigint
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


ALTER FUNCTION carga_org_lot.sp_insert_lotacao_json_orgao(p_idlotacaoversao bigint, p_idorganogramaversao bigint, p_idpatriarca bigint, p_idorgaolotacao bigint, p_jsconteudo jsonb) OWNER TO postgres;

--
-- TOC entry 318 (class 1255 OID 18108)
-- Name: sp_insert_lotacao_versao(bigint, text, text, text); Type: FUNCTION; Schema: carga_org_lot; Owner: postgres
--

CREATE FUNCTION carga_org_lot.sp_insert_lotacao_versao(p_idpatriarca bigint, p_strorigem text, p_strtipoarquivooriginal text, p_strnomearquivooriginal text) RETURNS bigint
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


ALTER FUNCTION carga_org_lot.sp_insert_lotacao_versao(p_idpatriarca bigint, p_strorigem text, p_strtipoarquivooriginal text, p_strnomearquivooriginal text) OWNER TO postgres;

--
-- TOC entry 310 (class 1255 OID 18109)
-- Name: sp_insert_organograma_json(bigint, jsonb); Type: FUNCTION; Schema: carga_org_lot; Owner: postgres
--

CREATE FUNCTION carga_org_lot.sp_insert_organograma_json(p_idorganogramaversao bigint, p_jsconteudo jsonb) RETURNS bigint
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


ALTER FUNCTION carga_org_lot.sp_insert_organograma_json(p_idorganogramaversao bigint, p_jsconteudo jsonb) OWNER TO postgres;

--
-- TOC entry 311 (class 1255 OID 18110)
-- Name: sp_insert_patriarca(uuid, text, text, integer, bigint); Type: FUNCTION; Schema: carga_org_lot; Owner: postgres
--

CREATE FUNCTION carga_org_lot.sp_insert_patriarca(p_idexternopatriarca uuid, p_strsiglapatriarca text, p_strnome text, p_idstatusprogresso integer, p_idusuariocriacao bigint) RETURNS bigint
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


ALTER FUNCTION carga_org_lot.sp_insert_patriarca(p_idexternopatriarca uuid, p_strsiglapatriarca text, p_strnome text, p_idstatusprogresso integer, p_idusuariocriacao bigint) OWNER TO postgres;

--
-- TOC entry 314 (class 1255 OID 18102)
-- Name: sp_insert_status_carga(integer, text, integer); Type: FUNCTION; Schema: carga_org_lot; Owner: postgres
--

CREATE FUNCTION carga_org_lot.sp_insert_status_carga(p_idstatuscarga integer, p_strdescricao text, p_flgsucesso integer) RETURNS bigint
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


ALTER FUNCTION carga_org_lot.sp_insert_status_carga(p_idstatuscarga integer, p_strdescricao text, p_flgsucesso integer) OWNER TO postgres;

--
-- TOC entry 315 (class 1255 OID 18101)
-- Name: sp_insert_tipo_carga(integer, text); Type: FUNCTION; Schema: carga_org_lot; Owner: postgres
--

CREATE FUNCTION carga_org_lot.sp_insert_tipo_carga(p_idtipocarga integer, p_strdescricao text) RETURNS bigint
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


ALTER FUNCTION carga_org_lot.sp_insert_tipo_carga(p_idtipocarga integer, p_strdescricao text) OWNER TO postgres;

--
-- TOC entry 316 (class 1255 OID 18100)
-- Name: sp_insert_token_envio_carga(bigint, integer, text); Type: FUNCTION; Schema: carga_org_lot; Owner: postgres
--

CREATE FUNCTION carga_org_lot.sp_insert_token_envio_carga(p_idpatriarca bigint, p_idstatustokenenviocarga integer, p_strtokenretorno text) RETURNS bigint
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


ALTER FUNCTION carga_org_lot.sp_insert_token_envio_carga(p_idpatriarca bigint, p_idstatustokenenviocarga integer, p_strtokenretorno text) OWNER TO postgres;

--
-- TOC entry 319 (class 1255 OID 18099)
-- Name: sp_set_organograma_versao_ativa(bigint, bigint); Type: FUNCTION; Schema: carga_org_lot; Owner: postgres
--

CREATE FUNCTION carga_org_lot.sp_set_organograma_versao_ativa(p_idpatriarca bigint, p_idorganogramaversao bigint) RETURNS bigint
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


ALTER FUNCTION carga_org_lot.sp_set_organograma_versao_ativa(p_idpatriarca bigint, p_idorganogramaversao bigint) OWNER TO postgres;

--
-- TOC entry 317 (class 1255 OID 18098)
-- Name: sp_update_patriarca(bigint, text, integer, bigint); Type: FUNCTION; Schema: carga_org_lot; Owner: postgres
--

CREATE FUNCTION carga_org_lot.sp_update_patriarca(p_idpatriarca bigint, p_strnome text, p_idstatusprogresso integer, p_idusuarioalteracao bigint) RETURNS bigint
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


ALTER FUNCTION carga_org_lot.sp_update_patriarca(p_idpatriarca bigint, p_strnome text, p_idstatusprogresso integer, p_idusuarioalteracao bigint) OWNER TO postgres;

--
-- TOC entry 301 (class 1255 OID 17356)
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
-- TOC entry 300 (class 1255 OID 17355)
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
-- TOC entry 305 (class 1255 OID 17359)
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
-- TOC entry 303 (class 1255 OID 17370)
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
-- TOC entry 304 (class 1255 OID 17371)
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
-- TOC entry 281 (class 1259 OID 18042)
-- Name: tbleixos; Type: TABLE; Schema: acoes_pngi; Owner: postgres
--

CREATE TABLE acoes_pngi.tbleixos (
    ideixo integer NOT NULL,
    strdescricaoeixo character varying(100) NOT NULL,
    stralias character varying(5) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE acoes_pngi.tbleixos OWNER TO postgres;

--
-- TOC entry 5567 (class 0 OID 0)
-- Dependencies: 281
-- Name: TABLE tbleixos; Type: COMMENT; Schema: acoes_pngi; Owner: postgres
--

COMMENT ON TABLE acoes_pngi.tbleixos IS 'Eixos estratégicos do PNGI';


--
-- TOC entry 280 (class 1259 OID 18041)
-- Name: tbleixos_ideixo_seq; Type: SEQUENCE; Schema: acoes_pngi; Owner: postgres
--

CREATE SEQUENCE acoes_pngi.tbleixos_ideixo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE acoes_pngi.tbleixos_ideixo_seq OWNER TO postgres;

--
-- TOC entry 5569 (class 0 OID 0)
-- Dependencies: 280
-- Name: tbleixos_ideixo_seq; Type: SEQUENCE OWNED BY; Schema: acoes_pngi; Owner: postgres
--

ALTER SEQUENCE acoes_pngi.tbleixos_ideixo_seq OWNED BY acoes_pngi.tbleixos.ideixo;


--
-- TOC entry 283 (class 1259 OID 18056)
-- Name: tblsituacaoacao; Type: TABLE; Schema: acoes_pngi; Owner: postgres
--

CREATE TABLE acoes_pngi.tblsituacaoacao (
    idsituacaoacao integer NOT NULL,
    strdescricaosituacao character varying(15) NOT NULL
);


ALTER TABLE acoes_pngi.tblsituacaoacao OWNER TO postgres;

--
-- TOC entry 5571 (class 0 OID 0)
-- Dependencies: 283
-- Name: TABLE tblsituacaoacao; Type: COMMENT; Schema: acoes_pngi; Owner: postgres
--

COMMENT ON TABLE acoes_pngi.tblsituacaoacao IS 'Situações possíveis de uma ação PNGI';


--
-- TOC entry 282 (class 1259 OID 18055)
-- Name: tblsituacaoacao_idsituacaoacao_seq; Type: SEQUENCE; Schema: acoes_pngi; Owner: postgres
--

CREATE SEQUENCE acoes_pngi.tblsituacaoacao_idsituacaoacao_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE acoes_pngi.tblsituacaoacao_idsituacaoacao_seq OWNER TO postgres;

--
-- TOC entry 5573 (class 0 OID 0)
-- Dependencies: 282
-- Name: tblsituacaoacao_idsituacaoacao_seq; Type: SEQUENCE OWNED BY; Schema: acoes_pngi; Owner: postgres
--

ALTER SEQUENCE acoes_pngi.tblsituacaoacao_idsituacaoacao_seq OWNED BY acoes_pngi.tblsituacaoacao.idsituacaoacao;


--
-- TOC entry 285 (class 1259 OID 18067)
-- Name: tblvigenciapngi; Type: TABLE; Schema: acoes_pngi; Owner: postgres
--

CREATE TABLE acoes_pngi.tblvigenciapngi (
    idvigenciapngi integer NOT NULL,
    strdescricaovigenciapngi character varying(100) NOT NULL,
    datiniciovigencia date NOT NULL,
    datfinalvigencia date NOT NULL,
    isvigenciaativa boolean DEFAULT false,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_vigencia_datas CHECK ((datfinalvigencia > datiniciovigencia))
);


ALTER TABLE acoes_pngi.tblvigenciapngi OWNER TO postgres;

--
-- TOC entry 5575 (class 0 OID 0)
-- Dependencies: 285
-- Name: TABLE tblvigenciapngi; Type: COMMENT; Schema: acoes_pngi; Owner: postgres
--

COMMENT ON TABLE acoes_pngi.tblvigenciapngi IS 'Períodos de vigência do PNGI';


--
-- TOC entry 284 (class 1259 OID 18066)
-- Name: tblvigenciapngi_idvigenciapngi_seq; Type: SEQUENCE; Schema: acoes_pngi; Owner: postgres
--

CREATE SEQUENCE acoes_pngi.tblvigenciapngi_idvigenciapngi_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE acoes_pngi.tblvigenciapngi_idvigenciapngi_seq OWNER TO postgres;

--
-- TOC entry 5577 (class 0 OID 0)
-- Dependencies: 284
-- Name: tblvigenciapngi_idvigenciapngi_seq; Type: SEQUENCE OWNED BY; Schema: acoes_pngi; Owner: postgres
--

ALTER SEQUENCE acoes_pngi.tblvigenciapngi_idvigenciapngi_seq OWNED BY acoes_pngi.tblvigenciapngi.idvigenciapngi;


--
-- TOC entry 235 (class 1259 OID 17038)
-- Name: tblcargapatriarca; Type: TABLE; Schema: carga_org_lot; Owner: postgres
--

CREATE TABLE carga_org_lot.tblcargapatriarca (
    idcargapatriarca bigint NOT NULL,
    idpatriarca bigint NOT NULL,
    idtokenenviocarga bigint NOT NULL,
    idstatuscarga smallint NOT NULL,
    idtipocarga smallint NOT NULL,
    strmensagemretorno text,
    datdatahorainicio timestamp with time zone DEFAULT now() NOT NULL,
    datdatahorafim timestamp with time zone
);


ALTER TABLE carga_org_lot.tblcargapatriarca OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 17037)
-- Name: tblcargapatriarca_idcargapatriarca_seq; Type: SEQUENCE; Schema: carga_org_lot; Owner: postgres
--

CREATE SEQUENCE carga_org_lot.tblcargapatriarca_idcargapatriarca_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE carga_org_lot.tblcargapatriarca_idcargapatriarca_seq OWNER TO postgres;

--
-- TOC entry 5579 (class 0 OID 0)
-- Dependencies: 234
-- Name: tblcargapatriarca_idcargapatriarca_seq; Type: SEQUENCE OWNED BY; Schema: carga_org_lot; Owner: postgres
--

ALTER SEQUENCE carga_org_lot.tblcargapatriarca_idcargapatriarca_seq OWNED BY carga_org_lot.tblcargapatriarca.idcargapatriarca;


--
-- TOC entry 237 (class 1259 OID 17075)
-- Name: tbldetalhestatuscarga; Type: TABLE; Schema: carga_org_lot; Owner: postgres
--

CREATE TABLE carga_org_lot.tbldetalhestatuscarga (
    iddetalhestatuscarga bigint NOT NULL,
    idcargapatriarca bigint NOT NULL,
    idstatuscarga smallint NOT NULL,
    datregistro timestamp with time zone DEFAULT now() NOT NULL,
    strmensagem text
);


ALTER TABLE carga_org_lot.tbldetalhestatuscarga OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 17074)
-- Name: tbldetalhestatuscarga_iddetalhestatuscarga_seq; Type: SEQUENCE; Schema: carga_org_lot; Owner: postgres
--

CREATE SEQUENCE carga_org_lot.tbldetalhestatuscarga_iddetalhestatuscarga_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE carga_org_lot.tbldetalhestatuscarga_iddetalhestatuscarga_seq OWNER TO postgres;

--
-- TOC entry 5581 (class 0 OID 0)
-- Dependencies: 236
-- Name: tbldetalhestatuscarga_iddetalhestatuscarga_seq; Type: SEQUENCE OWNED BY; Schema: carga_org_lot; Owner: postgres
--

ALTER SEQUENCE carga_org_lot.tbldetalhestatuscarga_iddetalhestatuscarga_seq OWNED BY carga_org_lot.tbldetalhestatuscarga.iddetalhestatuscarga;


--
-- TOC entry 247 (class 1259 OID 17223)
-- Name: tbllotacao; Type: TABLE; Schema: carga_org_lot; Owner: postgres
--

CREATE TABLE carga_org_lot.tbllotacao (
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


ALTER TABLE carga_org_lot.tbllotacao OWNER TO postgres;

--
-- TOC entry 246 (class 1259 OID 17222)
-- Name: tbllotacao_idlotacao_seq; Type: SEQUENCE; Schema: carga_org_lot; Owner: postgres
--

CREATE SEQUENCE carga_org_lot.tbllotacao_idlotacao_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE carga_org_lot.tbllotacao_idlotacao_seq OWNER TO postgres;

--
-- TOC entry 5583 (class 0 OID 0)
-- Dependencies: 246
-- Name: tbllotacao_idlotacao_seq; Type: SEQUENCE OWNED BY; Schema: carga_org_lot; Owner: postgres
--

ALTER SEQUENCE carga_org_lot.tbllotacao_idlotacao_seq OWNED BY carga_org_lot.tbllotacao.idlotacao;


--
-- TOC entry 251 (class 1259 OID 17320)
-- Name: tbllotacaoinconsistencia; Type: TABLE; Schema: carga_org_lot; Owner: postgres
--

CREATE TABLE carga_org_lot.tbllotacaoinconsistencia (
    idinconsistencia bigint NOT NULL,
    idlotacao bigint NOT NULL,
    strtipo character varying(100) NOT NULL,
    strdetalhe text NOT NULL,
    datregistro timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE carga_org_lot.tbllotacaoinconsistencia OWNER TO postgres;

--
-- TOC entry 250 (class 1259 OID 17319)
-- Name: tbllotacaoinconsistencia_idinconsistencia_seq; Type: SEQUENCE; Schema: carga_org_lot; Owner: postgres
--

CREATE SEQUENCE carga_org_lot.tbllotacaoinconsistencia_idinconsistencia_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE carga_org_lot.tbllotacaoinconsistencia_idinconsistencia_seq OWNER TO postgres;

--
-- TOC entry 5585 (class 0 OID 0)
-- Dependencies: 250
-- Name: tbllotacaoinconsistencia_idinconsistencia_seq; Type: SEQUENCE OWNED BY; Schema: carga_org_lot; Owner: postgres
--

ALTER SEQUENCE carga_org_lot.tbllotacaoinconsistencia_idinconsistencia_seq OWNED BY carga_org_lot.tbllotacaoinconsistencia.idinconsistencia;


--
-- TOC entry 249 (class 1259 OID 17280)
-- Name: tbllotacaojsonorgao; Type: TABLE; Schema: carga_org_lot; Owner: postgres
--

CREATE TABLE carga_org_lot.tbllotacaojsonorgao (
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


ALTER TABLE carga_org_lot.tbllotacaojsonorgao OWNER TO postgres;

--
-- TOC entry 248 (class 1259 OID 17279)
-- Name: tbllotacaojsonorgao_idlotacaojsonorgao_seq; Type: SEQUENCE; Schema: carga_org_lot; Owner: postgres
--

CREATE SEQUENCE carga_org_lot.tbllotacaojsonorgao_idlotacaojsonorgao_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE carga_org_lot.tbllotacaojsonorgao_idlotacaojsonorgao_seq OWNER TO postgres;

--
-- TOC entry 5587 (class 0 OID 0)
-- Dependencies: 248
-- Name: tbllotacaojsonorgao_idlotacaojsonorgao_seq; Type: SEQUENCE OWNED BY; Schema: carga_org_lot; Owner: postgres
--

ALTER SEQUENCE carga_org_lot.tbllotacaojsonorgao_idlotacaojsonorgao_seq OWNED BY carga_org_lot.tbllotacaojsonorgao.idlotacaojsonorgao;


--
-- TOC entry 245 (class 1259 OID 17192)
-- Name: tbllotacaoversao; Type: TABLE; Schema: carga_org_lot; Owner: postgres
--

CREATE TABLE carga_org_lot.tbllotacaoversao (
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


ALTER TABLE carga_org_lot.tbllotacaoversao OWNER TO postgres;

--
-- TOC entry 244 (class 1259 OID 17191)
-- Name: tbllotacaoversao_idlotacaoversao_seq; Type: SEQUENCE; Schema: carga_org_lot; Owner: postgres
--

CREATE SEQUENCE carga_org_lot.tbllotacaoversao_idlotacaoversao_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE carga_org_lot.tbllotacaoversao_idlotacaoversao_seq OWNER TO postgres;

--
-- TOC entry 5589 (class 0 OID 0)
-- Dependencies: 244
-- Name: tbllotacaoversao_idlotacaoversao_seq; Type: SEQUENCE OWNED BY; Schema: carga_org_lot; Owner: postgres
--

ALTER SEQUENCE carga_org_lot.tbllotacaoversao_idlotacaoversao_seq OWNED BY carga_org_lot.tbllotacaoversao.idlotacaoversao;


--
-- TOC entry 243 (class 1259 OID 17172)
-- Name: tblorganogramajson; Type: TABLE; Schema: carga_org_lot; Owner: postgres
--

CREATE TABLE carga_org_lot.tblorganogramajson (
    idorganogramajson bigint NOT NULL,
    idorganogramaversao bigint NOT NULL,
    jsconteudo jsonb NOT NULL,
    datcriacao timestamp with time zone DEFAULT now() NOT NULL,
    datenvioapi timestamp with time zone,
    strstatusenvio character varying(30),
    strmensagemretorno text
);


ALTER TABLE carga_org_lot.tblorganogramajson OWNER TO postgres;

--
-- TOC entry 242 (class 1259 OID 17171)
-- Name: tblorganogramajson_idorganogramajson_seq; Type: SEQUENCE; Schema: carga_org_lot; Owner: postgres
--

CREATE SEQUENCE carga_org_lot.tblorganogramajson_idorganogramajson_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE carga_org_lot.tblorganogramajson_idorganogramajson_seq OWNER TO postgres;

--
-- TOC entry 5591 (class 0 OID 0)
-- Dependencies: 242
-- Name: tblorganogramajson_idorganogramajson_seq; Type: SEQUENCE OWNED BY; Schema: carga_org_lot; Owner: postgres
--

ALTER SEQUENCE carga_org_lot.tblorganogramajson_idorganogramajson_seq OWNED BY carga_org_lot.tblorganogramajson.idorganogramajson;


--
-- TOC entry 239 (class 1259 OID 17102)
-- Name: tblorganogramaversao; Type: TABLE; Schema: carga_org_lot; Owner: postgres
--

CREATE TABLE carga_org_lot.tblorganogramaversao (
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


ALTER TABLE carga_org_lot.tblorganogramaversao OWNER TO postgres;

--
-- TOC entry 238 (class 1259 OID 17101)
-- Name: tblorganogramaversao_idorganogramaversao_seq; Type: SEQUENCE; Schema: carga_org_lot; Owner: postgres
--

CREATE SEQUENCE carga_org_lot.tblorganogramaversao_idorganogramaversao_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE carga_org_lot.tblorganogramaversao_idorganogramaversao_seq OWNER TO postgres;

--
-- TOC entry 5593 (class 0 OID 0)
-- Dependencies: 238
-- Name: tblorganogramaversao_idorganogramaversao_seq; Type: SEQUENCE OWNED BY; Schema: carga_org_lot; Owner: postgres
--

ALTER SEQUENCE carga_org_lot.tblorganogramaversao_idorganogramaversao_seq OWNED BY carga_org_lot.tblorganogramaversao.idorganogramaversao;


--
-- TOC entry 241 (class 1259 OID 17126)
-- Name: tblorgaounidade; Type: TABLE; Schema: carga_org_lot; Owner: postgres
--

CREATE TABLE carga_org_lot.tblorgaounidade (
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


ALTER TABLE carga_org_lot.tblorgaounidade OWNER TO postgres;

--
-- TOC entry 240 (class 1259 OID 17125)
-- Name: tblorgaounidade_idorgaounidade_seq; Type: SEQUENCE; Schema: carga_org_lot; Owner: postgres
--

CREATE SEQUENCE carga_org_lot.tblorgaounidade_idorgaounidade_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE carga_org_lot.tblorgaounidade_idorgaounidade_seq OWNER TO postgres;

--
-- TOC entry 5595 (class 0 OID 0)
-- Dependencies: 240
-- Name: tblorgaounidade_idorgaounidade_seq; Type: SEQUENCE OWNED BY; Schema: carga_org_lot; Owner: postgres
--

ALTER SEQUENCE carga_org_lot.tblorgaounidade_idorgaounidade_seq OWNED BY carga_org_lot.tblorgaounidade.idorgaounidade;


--
-- TOC entry 228 (class 1259 OID 16953)
-- Name: tblpatriarca; Type: TABLE; Schema: carga_org_lot; Owner: postgres
--

CREATE TABLE carga_org_lot.tblpatriarca (
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


ALTER TABLE carga_org_lot.tblpatriarca OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16952)
-- Name: tblpatriarca_idpatriarca_seq; Type: SEQUENCE; Schema: carga_org_lot; Owner: postgres
--

CREATE SEQUENCE carga_org_lot.tblpatriarca_idpatriarca_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE carga_org_lot.tblpatriarca_idpatriarca_seq OWNER TO postgres;

--
-- TOC entry 5597 (class 0 OID 0)
-- Dependencies: 227
-- Name: tblpatriarca_idpatriarca_seq; Type: SEQUENCE OWNED BY; Schema: carga_org_lot; Owner: postgres
--

ALTER SEQUENCE carga_org_lot.tblpatriarca_idpatriarca_seq OWNED BY carga_org_lot.tblpatriarca.idpatriarca;


--
-- TOC entry 233 (class 1259 OID 17029)
-- Name: tblstatuscarga; Type: TABLE; Schema: carga_org_lot; Owner: postgres
--

CREATE TABLE carga_org_lot.tblstatuscarga (
    idstatuscarga smallint NOT NULL,
    strdescricao character varying(150) NOT NULL,
    flgsucesso integer NOT NULL
);


ALTER TABLE carga_org_lot.tblstatuscarga OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 16945)
-- Name: tblstatusprogresso; Type: TABLE; Schema: carga_org_lot; Owner: postgres
--

CREATE TABLE carga_org_lot.tblstatusprogresso (
    idstatusprogresso smallint NOT NULL,
    strdescricao character varying(100) NOT NULL
);


ALTER TABLE carga_org_lot.tblstatusprogresso OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16989)
-- Name: tblstatustokenenviocarga; Type: TABLE; Schema: carga_org_lot; Owner: postgres
--

CREATE TABLE carga_org_lot.tblstatustokenenviocarga (
    idstatustokenenviocarga smallint NOT NULL,
    strdescricao character varying(100) NOT NULL
);


ALTER TABLE carga_org_lot.tblstatustokenenviocarga OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 17022)
-- Name: tbltipocarga; Type: TABLE; Schema: carga_org_lot; Owner: postgres
--

CREATE TABLE carga_org_lot.tbltipocarga (
    idtipocarga smallint NOT NULL,
    strdescricao character varying(100) NOT NULL
);


ALTER TABLE carga_org_lot.tbltipocarga OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16997)
-- Name: tbltokenenviocarga; Type: TABLE; Schema: carga_org_lot; Owner: postgres
--

CREATE TABLE carga_org_lot.tbltokenenviocarga (
    idtokenenviocarga bigint NOT NULL,
    idpatriarca bigint NOT NULL,
    idstatustokenenviocarga smallint NOT NULL,
    strtokenretorno character varying(1000) NOT NULL,
    datdatahorainicio timestamp with time zone DEFAULT now() NOT NULL,
    datdatahorafim timestamp with time zone
);


ALTER TABLE carga_org_lot.tbltokenenviocarga OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 16996)
-- Name: tbltokenenviocarga_idtokenenviocarga_seq; Type: SEQUENCE; Schema: carga_org_lot; Owner: postgres
--

CREATE SEQUENCE carga_org_lot.tbltokenenviocarga_idtokenenviocarga_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE carga_org_lot.tbltokenenviocarga_idtokenenviocarga_seq OWNER TO postgres;

--
-- TOC entry 5599 (class 0 OID 0)
-- Dependencies: 230
-- Name: tbltokenenviocarga_idtokenenviocarga_seq; Type: SEQUENCE OWNED BY; Schema: carga_org_lot; Owner: postgres
--

ALTER SEQUENCE carga_org_lot.tbltokenenviocarga_idtokenenviocarga_seq OWNED BY carga_org_lot.tbltokenenviocarga.idtokenenviocarga;


--
-- TOC entry 267 (class 1259 OID 17854)
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
-- TOC entry 266 (class 1259 OID 17853)
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
-- TOC entry 265 (class 1259 OID 17844)
-- Name: accounts_role; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts_role (
    id bigint NOT NULL,
    nomeperfil character varying(100) NOT NULL,
    codigoperfil character varying(100) NOT NULL,
    aplicacao_id integer
);


ALTER TABLE public.accounts_role OWNER TO postgres;

--
-- TOC entry 264 (class 1259 OID 17843)
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
-- TOC entry 287 (class 1259 OID 58150)
-- Name: accounts_rolepermission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts_rolepermission (
    id bigint NOT NULL,
    permission_id integer NOT NULL,
    role_id bigint NOT NULL
);


ALTER TABLE public.accounts_rolepermission OWNER TO postgres;

--
-- TOC entry 286 (class 1259 OID 58149)
-- Name: accounts_rolepermission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.accounts_rolepermission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.accounts_rolepermission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 269 (class 1259 OID 17864)
-- Name: accounts_userrole; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts_userrole (
    id bigint NOT NULL,
    aplicacao_id integer,
    role_id bigint NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.accounts_userrole OWNER TO postgres;

--
-- TOC entry 268 (class 1259 OID 17863)
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
-- TOC entry 261 (class 1259 OID 17795)
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- TOC entry 260 (class 1259 OID 17794)
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
-- TOC entry 263 (class 1259 OID 17805)
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- TOC entry 262 (class 1259 OID 17804)
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
-- TOC entry 259 (class 1259 OID 17785)
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
-- TOC entry 258 (class 1259 OID 17784)
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
-- TOC entry 272 (class 1259 OID 17942)
-- Name: authtoken_token; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.authtoken_token (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.authtoken_token OWNER TO postgres;

--
-- TOC entry 274 (class 1259 OID 17959)
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
-- TOC entry 273 (class 1259 OID 17958)
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
-- TOC entry 271 (class 1259 OID 17916)
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
-- TOC entry 270 (class 1259 OID 17915)
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
-- TOC entry 257 (class 1259 OID 17773)
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- TOC entry 256 (class 1259 OID 17772)
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
-- TOC entry 255 (class 1259 OID 17761)
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
-- TOC entry 254 (class 1259 OID 17760)
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
-- TOC entry 275 (class 1259 OID 17979)
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- TOC entry 253 (class 1259 OID 17738)
-- Name: tblaplicacao; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tblaplicacao (
    idaplicacao bigint CONSTRAINT tblaplicacao_idapplication_not_null NOT NULL,
    codigointerno character varying(50) CONSTRAINT tblaplicacao_code_not_null NOT NULL,
    nomeaplicacao character varying(200) CONSTRAINT tblaplicacao_name_not_null NOT NULL,
    base_url character varying(500),
    isshowinportal boolean DEFAULT false
);


ALTER TABLE public.tblaplicacao OWNER TO postgres;

--
-- TOC entry 252 (class 1259 OID 17737)
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
-- TOC entry 5612 (class 0 OID 0)
-- Dependencies: 252
-- Name: tblaplicacao_idapplication_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tblaplicacao_idapplication_seq OWNED BY public.tblaplicacao.idaplicacao;


--
-- TOC entry 223 (class 1259 OID 16893)
-- Name: tblclassificacaousuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tblclassificacaousuario (
    idclassificacaousuario smallint NOT NULL,
    strdescricao character varying(100) NOT NULL
);


ALTER TABLE public.tblclassificacaousuario OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16879)
-- Name: tblstatususuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tblstatususuario (
    idstatususuario smallint NOT NULL,
    strdescricao character varying(100) NOT NULL
);


ALTER TABLE public.tblstatususuario OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16886)
-- Name: tbltipousuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbltipousuario (
    idtipousuario smallint NOT NULL,
    strdescricao character varying(100) NOT NULL
);


ALTER TABLE public.tbltipousuario OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16901)
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
-- TOC entry 277 (class 1259 OID 17993)
-- Name: tblusuario_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tblusuario_groups (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.tblusuario_groups OWNER TO postgres;

--
-- TOC entry 276 (class 1259 OID 17992)
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
-- TOC entry 5618 (class 0 OID 0)
-- Dependencies: 276
-- Name: tblusuario_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tblusuario_groups_id_seq OWNED BY public.tblusuario_groups.id;


--
-- TOC entry 224 (class 1259 OID 16900)
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
-- TOC entry 5619 (class 0 OID 0)
-- Dependencies: 224
-- Name: tblusuario_idusuario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tblusuario_idusuario_seq OWNED BY public.tblusuario.idusuario;


--
-- TOC entry 279 (class 1259 OID 18015)
-- Name: tblusuario_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tblusuario_user_permissions (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.tblusuario_user_permissions OWNER TO postgres;

--
-- TOC entry 278 (class 1259 OID 18014)
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
-- TOC entry 5621 (class 0 OID 0)
-- Dependencies: 278
-- Name: tblusuario_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tblusuario_user_permissions_id_seq OWNED BY public.tblusuario_user_permissions.id;


--
-- TOC entry 5098 (class 2604 OID 18045)
-- Name: tbleixos ideixo; Type: DEFAULT; Schema: acoes_pngi; Owner: postgres
--

ALTER TABLE ONLY acoes_pngi.tbleixos ALTER COLUMN ideixo SET DEFAULT nextval('acoes_pngi.tbleixos_ideixo_seq'::regclass);


--
-- TOC entry 5101 (class 2604 OID 18059)
-- Name: tblsituacaoacao idsituacaoacao; Type: DEFAULT; Schema: acoes_pngi; Owner: postgres
--

ALTER TABLE ONLY acoes_pngi.tblsituacaoacao ALTER COLUMN idsituacaoacao SET DEFAULT nextval('acoes_pngi.tblsituacaoacao_idsituacaoacao_seq'::regclass);


--
-- TOC entry 5102 (class 2604 OID 18070)
-- Name: tblvigenciapngi idvigenciapngi; Type: DEFAULT; Schema: acoes_pngi; Owner: postgres
--

ALTER TABLE ONLY acoes_pngi.tblvigenciapngi ALTER COLUMN idvigenciapngi SET DEFAULT nextval('acoes_pngi.tblvigenciapngi_idvigenciapngi_seq'::regclass);


--
-- TOC entry 5070 (class 2604 OID 17041)
-- Name: tblcargapatriarca idcargapatriarca; Type: DEFAULT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblcargapatriarca ALTER COLUMN idcargapatriarca SET DEFAULT nextval('carga_org_lot.tblcargapatriarca_idcargapatriarca_seq'::regclass);


--
-- TOC entry 5072 (class 2604 OID 17078)
-- Name: tbldetalhestatuscarga iddetalhestatuscarga; Type: DEFAULT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbldetalhestatuscarga ALTER COLUMN iddetalhestatuscarga SET DEFAULT nextval('carga_org_lot.tbldetalhestatuscarga_iddetalhestatuscarga_seq'::regclass);


--
-- TOC entry 5087 (class 2604 OID 17226)
-- Name: tbllotacao idlotacao; Type: DEFAULT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbllotacao ALTER COLUMN idlotacao SET DEFAULT nextval('carga_org_lot.tbllotacao_idlotacao_seq'::regclass);


--
-- TOC entry 5092 (class 2604 OID 17323)
-- Name: tbllotacaoinconsistencia idinconsistencia; Type: DEFAULT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbllotacaoinconsistencia ALTER COLUMN idinconsistencia SET DEFAULT nextval('carga_org_lot.tbllotacaoinconsistencia_idinconsistencia_seq'::regclass);


--
-- TOC entry 5090 (class 2604 OID 17283)
-- Name: tbllotacaojsonorgao idlotacaojsonorgao; Type: DEFAULT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbllotacaojsonorgao ALTER COLUMN idlotacaojsonorgao SET DEFAULT nextval('carga_org_lot.tbllotacaojsonorgao_idlotacaojsonorgao_seq'::regclass);


--
-- TOC entry 5083 (class 2604 OID 17195)
-- Name: tbllotacaoversao idlotacaoversao; Type: DEFAULT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbllotacaoversao ALTER COLUMN idlotacaoversao SET DEFAULT nextval('carga_org_lot.tbllotacaoversao_idlotacaoversao_seq'::regclass);


--
-- TOC entry 5081 (class 2604 OID 17175)
-- Name: tblorganogramajson idorganogramajson; Type: DEFAULT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblorganogramajson ALTER COLUMN idorganogramajson SET DEFAULT nextval('carga_org_lot.tblorganogramajson_idorganogramajson_seq'::regclass);


--
-- TOC entry 5074 (class 2604 OID 17105)
-- Name: tblorganogramaversao idorganogramaversao; Type: DEFAULT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblorganogramaversao ALTER COLUMN idorganogramaversao SET DEFAULT nextval('carga_org_lot.tblorganogramaversao_idorganogramaversao_seq'::regclass);


--
-- TOC entry 5078 (class 2604 OID 17129)
-- Name: tblorgaounidade idorgaounidade; Type: DEFAULT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblorgaounidade ALTER COLUMN idorgaounidade SET DEFAULT nextval('carga_org_lot.tblorgaounidade_idorgaounidade_seq'::regclass);


--
-- TOC entry 5066 (class 2604 OID 16956)
-- Name: tblpatriarca idpatriarca; Type: DEFAULT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblpatriarca ALTER COLUMN idpatriarca SET DEFAULT nextval('carga_org_lot.tblpatriarca_idpatriarca_seq'::regclass);


--
-- TOC entry 5068 (class 2604 OID 17000)
-- Name: tbltokenenviocarga idtokenenviocarga; Type: DEFAULT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbltokenenviocarga ALTER COLUMN idtokenenviocarga SET DEFAULT nextval('carga_org_lot.tbltokenenviocarga_idtokenenviocarga_seq'::regclass);


--
-- TOC entry 5094 (class 2604 OID 17741)
-- Name: tblaplicacao idaplicacao; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblaplicacao ALTER COLUMN idaplicacao SET DEFAULT nextval('public.tblaplicacao_idapplication_seq'::regclass);


--
-- TOC entry 5060 (class 2604 OID 16904)
-- Name: tblusuario idusuario; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario ALTER COLUMN idusuario SET DEFAULT nextval('public.tblusuario_idusuario_seq'::regclass);


--
-- TOC entry 5096 (class 2604 OID 17996)
-- Name: tblusuario_groups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario_groups ALTER COLUMN id SET DEFAULT nextval('public.tblusuario_groups_id_seq'::regclass);


--
-- TOC entry 5097 (class 2604 OID 18018)
-- Name: tblusuario_user_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.tblusuario_user_permissions_id_seq'::regclass);


--
-- TOC entry 5536 (class 0 OID 18042)
-- Dependencies: 281
-- Data for Name: tbleixos; Type: TABLE DATA; Schema: acoes_pngi; Owner: postgres
--

INSERT INTO acoes_pngi.tbleixos VALUES (1, 'Transformação Digital', 'TD', '2026-01-14 16:22:24.768642', '2026-01-14 16:22:24.768642');
INSERT INTO acoes_pngi.tbleixos VALUES (2, 'Transferências e Parcerias', 'TP', '2026-01-14 16:22:24.768642', '2026-01-14 16:22:24.768642');
INSERT INTO acoes_pngi.tbleixos VALUES (3, 'Inovação e Desenvolvimento de Competências e Lideranças', 'IDCL', '2026-01-14 16:22:24.768642', '2026-01-14 16:22:24.768642');
INSERT INTO acoes_pngi.tbleixos VALUES (4, 'Patrimônio Imobiliário e Responsabilidade Socioambiental', 'PIRS', '2026-01-14 16:22:24.768642', '2026-01-14 16:22:24.768642');
INSERT INTO acoes_pngi.tbleixos VALUES (5, 'Logística e Compras Públicas', 'LCP', '2026-01-14 16:22:24.768642', '2026-01-14 16:22:24.768642');


--
-- TOC entry 5538 (class 0 OID 18056)
-- Dependencies: 283
-- Data for Name: tblsituacaoacao; Type: TABLE DATA; Schema: acoes_pngi; Owner: postgres
--

INSERT INTO acoes_pngi.tblsituacaoacao VALUES (1, 'ATRASADA');
INSERT INTO acoes_pngi.tblsituacaoacao VALUES (2, 'CONCLUÍDA');
INSERT INTO acoes_pngi.tblsituacaoacao VALUES (3, 'REPACTUADA');
INSERT INTO acoes_pngi.tblsituacaoacao VALUES (4, 'EM ANDAMENTO');
INSERT INTO acoes_pngi.tblsituacaoacao VALUES (5, 'CANCELADA');
INSERT INTO acoes_pngi.tblsituacaoacao VALUES (6, 'NÃO INICIADA');
INSERT INTO acoes_pngi.tblsituacaoacao VALUES (7, 'AGUARDANDO FEED');


--
-- TOC entry 5540 (class 0 OID 18067)
-- Dependencies: 285
-- Data for Name: tblvigenciapngi; Type: TABLE DATA; Schema: acoes_pngi; Owner: postgres
--



--
-- TOC entry 5490 (class 0 OID 17038)
-- Dependencies: 235
-- Data for Name: tblcargapatriarca; Type: TABLE DATA; Schema: carga_org_lot; Owner: postgres
--



--
-- TOC entry 5492 (class 0 OID 17075)
-- Dependencies: 237
-- Data for Name: tbldetalhestatuscarga; Type: TABLE DATA; Schema: carga_org_lot; Owner: postgres
--



--
-- TOC entry 5502 (class 0 OID 17223)
-- Dependencies: 247
-- Data for Name: tbllotacao; Type: TABLE DATA; Schema: carga_org_lot; Owner: postgres
--



--
-- TOC entry 5506 (class 0 OID 17320)
-- Dependencies: 251
-- Data for Name: tbllotacaoinconsistencia; Type: TABLE DATA; Schema: carga_org_lot; Owner: postgres
--



--
-- TOC entry 5504 (class 0 OID 17280)
-- Dependencies: 249
-- Data for Name: tbllotacaojsonorgao; Type: TABLE DATA; Schema: carga_org_lot; Owner: postgres
--



--
-- TOC entry 5500 (class 0 OID 17192)
-- Dependencies: 245
-- Data for Name: tbllotacaoversao; Type: TABLE DATA; Schema: carga_org_lot; Owner: postgres
--



--
-- TOC entry 5498 (class 0 OID 17172)
-- Dependencies: 243
-- Data for Name: tblorganogramajson; Type: TABLE DATA; Schema: carga_org_lot; Owner: postgres
--



--
-- TOC entry 5494 (class 0 OID 17102)
-- Dependencies: 239
-- Data for Name: tblorganogramaversao; Type: TABLE DATA; Schema: carga_org_lot; Owner: postgres
--



--
-- TOC entry 5496 (class 0 OID 17126)
-- Dependencies: 241
-- Data for Name: tblorgaounidade; Type: TABLE DATA; Schema: carga_org_lot; Owner: postgres
--



--
-- TOC entry 5483 (class 0 OID 16953)
-- Dependencies: 228
-- Data for Name: tblpatriarca; Type: TABLE DATA; Schema: carga_org_lot; Owner: postgres
--



--
-- TOC entry 5488 (class 0 OID 17029)
-- Dependencies: 233
-- Data for Name: tblstatuscarga; Type: TABLE DATA; Schema: carga_org_lot; Owner: postgres
--

INSERT INTO carga_org_lot.tblstatuscarga VALUES (1, 'Enviando Carga de Organograma', 0);
INSERT INTO carga_org_lot.tblstatuscarga VALUES (2, 'Organograma Enviado com sucesso', 1);
INSERT INTO carga_org_lot.tblstatuscarga VALUES (3, 'Organograma Enviado com Erro', 2);
INSERT INTO carga_org_lot.tblstatuscarga VALUES (4, 'Tempo Resposta Organograma Esgotado', 2);
INSERT INTO carga_org_lot.tblstatuscarga VALUES (5, 'Enviando Carga de Lotação', 0);
INSERT INTO carga_org_lot.tblstatuscarga VALUES (6, 'Lotação Enviada com sucesso', 1);
INSERT INTO carga_org_lot.tblstatuscarga VALUES (7, 'Lotação Enviada com Erro', 2);
INSERT INTO carga_org_lot.tblstatuscarga VALUES (8, 'Tempo Resposta Lotação Esgotado', 2);
INSERT INTO carga_org_lot.tblstatuscarga VALUES (9, 'Enviando Carga de Lotação (Arq. Único)', 0);
INSERT INTO carga_org_lot.tblstatuscarga VALUES (10, 'Lotação (Arq. Único) Enviada com sucesso', 1);
INSERT INTO carga_org_lot.tblstatuscarga VALUES (11, 'Lotação (Arq. Único) Enviada com Erro', 2);
INSERT INTO carga_org_lot.tblstatuscarga VALUES (12, 'Tempo Resposta Lotação (Arq. Único) Esgotado', 2);


--
-- TOC entry 5481 (class 0 OID 16945)
-- Dependencies: 226
-- Data for Name: tblstatusprogresso; Type: TABLE DATA; Schema: carga_org_lot; Owner: postgres
--

INSERT INTO carga_org_lot.tblstatusprogresso VALUES (1, 'Nova Carga');
INSERT INTO carga_org_lot.tblstatusprogresso VALUES (2, 'Organograma em Progresso');
INSERT INTO carga_org_lot.tblstatusprogresso VALUES (3, 'Lotação em Progresso');
INSERT INTO carga_org_lot.tblstatusprogresso VALUES (4, 'Pronto para Carga');
INSERT INTO carga_org_lot.tblstatusprogresso VALUES (5, 'Carga em Processamento');
INSERT INTO carga_org_lot.tblstatusprogresso VALUES (6, 'Carga Finalizada');


--
-- TOC entry 5484 (class 0 OID 16989)
-- Dependencies: 229
-- Data for Name: tblstatustokenenviocarga; Type: TABLE DATA; Schema: carga_org_lot; Owner: postgres
--

INSERT INTO carga_org_lot.tblstatustokenenviocarga VALUES (1, 'Solicitando Token');
INSERT INTO carga_org_lot.tblstatustokenenviocarga VALUES (2, 'Token Adquirido');
INSERT INTO carga_org_lot.tblstatustokenenviocarga VALUES (3, 'Token Negado');
INSERT INTO carga_org_lot.tblstatustokenenviocarga VALUES (4, 'Token Expirado');
INSERT INTO carga_org_lot.tblstatustokenenviocarga VALUES (5, 'Token Inválido');
INSERT INTO carga_org_lot.tblstatustokenenviocarga VALUES (6, 'Tempo Ultrapassado (Solicitação)');


--
-- TOC entry 5487 (class 0 OID 17022)
-- Dependencies: 232
-- Data for Name: tbltipocarga; Type: TABLE DATA; Schema: carga_org_lot; Owner: postgres
--

INSERT INTO carga_org_lot.tbltipocarga VALUES (1, 'Organograma');
INSERT INTO carga_org_lot.tbltipocarga VALUES (2, 'Lotação');
INSERT INTO carga_org_lot.tbltipocarga VALUES (3, 'Lotação Arq. Único');


--
-- TOC entry 5486 (class 0 OID 16997)
-- Dependencies: 231
-- Data for Name: tbltokenenviocarga; Type: TABLE DATA; Schema: carga_org_lot; Owner: postgres
--



--
-- TOC entry 5522 (class 0 OID 17854)
-- Dependencies: 267
-- Data for Name: accounts_attribute; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.accounts_attribute VALUES (1, 'can_upload', 'true', 2, 5);


--
-- TOC entry 5520 (class 0 OID 17844)
-- Dependencies: 265
-- Data for Name: accounts_role; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.accounts_role VALUES (4, 'Gestor do Portal', 'GESTOR_PORTAL', 1);
INSERT INTO public.accounts_role VALUES (5, 'Coordenador - Gerencia Configurações', 'COORDENADOR_PNGI', 3);
INSERT INTO public.accounts_role VALUES (6, 'Operador - Apenas Ações', 'OPERADOR_ACAO', 3);
INSERT INTO public.accounts_role VALUES (7, 'Consultor - Apenas Leitura', 'CONSULTOR_PNGI', 3);
INSERT INTO public.accounts_role VALUES (1, 'Usuário do Portal', 'USER_PORTAL', 1);
INSERT INTO public.accounts_role VALUES (2, 'Gestor Carga Org/Lot', 'GESTOR_CARGA', 2);
INSERT INTO public.accounts_role VALUES (3, 'Gestor Ações PNGI', 'GESTOR_PNGI', 3);


--
-- TOC entry 5542 (class 0 OID 58150)
-- Dependencies: 287
-- Data for Name: accounts_rolepermission; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.accounts_rolepermission VALUES (13, 53, 3);
INSERT INTO public.accounts_rolepermission VALUES (14, 54, 3);
INSERT INTO public.accounts_rolepermission VALUES (15, 55, 3);
INSERT INTO public.accounts_rolepermission VALUES (16, 56, 3);
INSERT INTO public.accounts_rolepermission VALUES (17, 57, 3);
INSERT INTO public.accounts_rolepermission VALUES (18, 58, 3);
INSERT INTO public.accounts_rolepermission VALUES (19, 59, 3);
INSERT INTO public.accounts_rolepermission VALUES (20, 60, 3);
INSERT INTO public.accounts_rolepermission VALUES (21, 61, 3);
INSERT INTO public.accounts_rolepermission VALUES (22, 62, 3);
INSERT INTO public.accounts_rolepermission VALUES (23, 63, 3);
INSERT INTO public.accounts_rolepermission VALUES (24, 64, 3);
INSERT INTO public.accounts_rolepermission VALUES (25, 53, 5);
INSERT INTO public.accounts_rolepermission VALUES (26, 54, 5);
INSERT INTO public.accounts_rolepermission VALUES (27, 56, 5);
INSERT INTO public.accounts_rolepermission VALUES (28, 57, 5);
INSERT INTO public.accounts_rolepermission VALUES (29, 58, 5);
INSERT INTO public.accounts_rolepermission VALUES (30, 60, 5);
INSERT INTO public.accounts_rolepermission VALUES (31, 61, 5);
INSERT INTO public.accounts_rolepermission VALUES (32, 62, 5);
INSERT INTO public.accounts_rolepermission VALUES (33, 64, 5);
INSERT INTO public.accounts_rolepermission VALUES (34, 56, 6);
INSERT INTO public.accounts_rolepermission VALUES (35, 60, 6);
INSERT INTO public.accounts_rolepermission VALUES (36, 64, 6);
INSERT INTO public.accounts_rolepermission VALUES (37, 56, 7);
INSERT INTO public.accounts_rolepermission VALUES (38, 60, 7);
INSERT INTO public.accounts_rolepermission VALUES (39, 64, 7);


--
-- TOC entry 5524 (class 0 OID 17864)
-- Dependencies: 269
-- Data for Name: accounts_userrole; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.accounts_userrole VALUES (1, 1, 1, 5);
INSERT INTO public.accounts_userrole VALUES (2, 2, 2, 5);
INSERT INTO public.accounts_userrole VALUES (3, 3, 3, 5);
INSERT INTO public.accounts_userrole VALUES (4, 1, 4, 5);
INSERT INTO public.accounts_userrole VALUES (5, 3, 5, 5);
INSERT INTO public.accounts_userrole VALUES (6, 3, 6, 5);
INSERT INTO public.accounts_userrole VALUES (7, 3, 7, 5);


--
-- TOC entry 5516 (class 0 OID 17795)
-- Dependencies: 261
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5518 (class 0 OID 17805)
-- Dependencies: 263
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5514 (class 0 OID 17785)
-- Dependencies: 259
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.auth_permission VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO public.auth_permission VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO public.auth_permission VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO public.auth_permission VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO public.auth_permission VALUES (5, 'Can add permission', 3, 'add_permission');
INSERT INTO public.auth_permission VALUES (6, 'Can change permission', 3, 'change_permission');
INSERT INTO public.auth_permission VALUES (7, 'Can delete permission', 3, 'delete_permission');
INSERT INTO public.auth_permission VALUES (8, 'Can view permission', 3, 'view_permission');
INSERT INTO public.auth_permission VALUES (9, 'Can add group', 2, 'add_group');
INSERT INTO public.auth_permission VALUES (10, 'Can change group', 2, 'change_group');
INSERT INTO public.auth_permission VALUES (11, 'Can delete group', 2, 'delete_group');
INSERT INTO public.auth_permission VALUES (12, 'Can view group', 2, 'view_group');
INSERT INTO public.auth_permission VALUES (13, 'Can add content type', 4, 'add_contenttype');
INSERT INTO public.auth_permission VALUES (14, 'Can change content type', 4, 'change_contenttype');
INSERT INTO public.auth_permission VALUES (15, 'Can delete content type', 4, 'delete_contenttype');
INSERT INTO public.auth_permission VALUES (16, 'Can view content type', 4, 'view_contenttype');
INSERT INTO public.auth_permission VALUES (17, 'Can add session', 5, 'add_session');
INSERT INTO public.auth_permission VALUES (18, 'Can change session', 5, 'change_session');
INSERT INTO public.auth_permission VALUES (19, 'Can delete session', 5, 'delete_session');
INSERT INTO public.auth_permission VALUES (20, 'Can view session', 5, 'view_session');
INSERT INTO public.auth_permission VALUES (21, 'Can add Token', 6, 'add_token');
INSERT INTO public.auth_permission VALUES (22, 'Can change Token', 6, 'change_token');
INSERT INTO public.auth_permission VALUES (23, 'Can delete Token', 6, 'delete_token');
INSERT INTO public.auth_permission VALUES (24, 'Can view Token', 6, 'view_token');
INSERT INTO public.auth_permission VALUES (25, 'Can add Token', 7, 'add_tokenproxy');
INSERT INTO public.auth_permission VALUES (26, 'Can change Token', 7, 'change_tokenproxy');
INSERT INTO public.auth_permission VALUES (27, 'Can delete Token', 7, 'delete_tokenproxy');
INSERT INTO public.auth_permission VALUES (28, 'Can view Token', 7, 'view_tokenproxy');
INSERT INTO public.auth_permission VALUES (29, 'Can add user', 11, 'add_user');
INSERT INTO public.auth_permission VALUES (30, 'Can change user', 11, 'change_user');
INSERT INTO public.auth_permission VALUES (31, 'Can delete user', 11, 'delete_user');
INSERT INTO public.auth_permission VALUES (32, 'Can view user', 11, 'view_user');
INSERT INTO public.auth_permission VALUES (33, 'Can add aplicacao', 8, 'add_aplicacao');
INSERT INTO public.auth_permission VALUES (34, 'Can change aplicacao', 8, 'change_aplicacao');
INSERT INTO public.auth_permission VALUES (35, 'Can delete aplicacao', 8, 'delete_aplicacao');
INSERT INTO public.auth_permission VALUES (36, 'Can view aplicacao', 8, 'view_aplicacao');
INSERT INTO public.auth_permission VALUES (37, 'Can add role', 10, 'add_role');
INSERT INTO public.auth_permission VALUES (38, 'Can change role', 10, 'change_role');
INSERT INTO public.auth_permission VALUES (39, 'Can delete role', 10, 'delete_role');
INSERT INTO public.auth_permission VALUES (40, 'Can view role', 10, 'view_role');
INSERT INTO public.auth_permission VALUES (41, 'Can add attribute', 9, 'add_attribute');
INSERT INTO public.auth_permission VALUES (42, 'Can change attribute', 9, 'change_attribute');
INSERT INTO public.auth_permission VALUES (43, 'Can delete attribute', 9, 'delete_attribute');
INSERT INTO public.auth_permission VALUES (44, 'Can view attribute', 9, 'view_attribute');
INSERT INTO public.auth_permission VALUES (45, 'Can add user role', 12, 'add_userrole');
INSERT INTO public.auth_permission VALUES (46, 'Can change user role', 12, 'change_userrole');
INSERT INTO public.auth_permission VALUES (47, 'Can delete user role', 12, 'delete_userrole');
INSERT INTO public.auth_permission VALUES (48, 'Can view user role', 12, 'view_userrole');
INSERT INTO public.auth_permission VALUES (49, 'Can add app client', 13, 'add_appclient');
INSERT INTO public.auth_permission VALUES (50, 'Can change app client', 13, 'change_appclient');
INSERT INTO public.auth_permission VALUES (51, 'Can delete app client', 13, 'delete_appclient');
INSERT INTO public.auth_permission VALUES (52, 'Can view app client', 13, 'view_appclient');
INSERT INTO public.auth_permission VALUES (53, 'Can add Eixo', 14, 'add_eixo');
INSERT INTO public.auth_permission VALUES (54, 'Can change Eixo', 14, 'change_eixo');
INSERT INTO public.auth_permission VALUES (55, 'Can delete Eixo', 14, 'delete_eixo');
INSERT INTO public.auth_permission VALUES (56, 'Can view Eixo', 14, 'view_eixo');
INSERT INTO public.auth_permission VALUES (57, 'Can add Situação de Ação', 15, 'add_situacaoacao');
INSERT INTO public.auth_permission VALUES (58, 'Can change Situação de Ação', 15, 'change_situacaoacao');
INSERT INTO public.auth_permission VALUES (59, 'Can delete Situação de Ação', 15, 'delete_situacaoacao');
INSERT INTO public.auth_permission VALUES (60, 'Can view Situação de Ação', 15, 'view_situacaoacao');
INSERT INTO public.auth_permission VALUES (61, 'Can add Vigência PNGI', 16, 'add_vigenciapngi');
INSERT INTO public.auth_permission VALUES (62, 'Can change Vigência PNGI', 16, 'change_vigenciapngi');
INSERT INTO public.auth_permission VALUES (63, 'Can delete Vigência PNGI', 16, 'delete_vigenciapngi');
INSERT INTO public.auth_permission VALUES (64, 'Can view Vigência PNGI', 16, 'view_vigenciapngi');
INSERT INTO public.auth_permission VALUES (65, 'Can add Carga Patriarca', 17, 'add_tblcargapatriarca');
INSERT INTO public.auth_permission VALUES (66, 'Can change Carga Patriarca', 17, 'change_tblcargapatriarca');
INSERT INTO public.auth_permission VALUES (67, 'Can delete Carga Patriarca', 17, 'delete_tblcargapatriarca');
INSERT INTO public.auth_permission VALUES (68, 'Can view Carga Patriarca', 17, 'view_tblcargapatriarca');
INSERT INTO public.auth_permission VALUES (69, 'Can add Detalhe Status Carga', 18, 'add_tbldetalhestatuscarga');
INSERT INTO public.auth_permission VALUES (70, 'Can change Detalhe Status Carga', 18, 'change_tbldetalhestatuscarga');
INSERT INTO public.auth_permission VALUES (71, 'Can delete Detalhe Status Carga', 18, 'delete_tbldetalhestatuscarga');
INSERT INTO public.auth_permission VALUES (72, 'Can view Detalhe Status Carga', 18, 'view_tbldetalhestatuscarga');
INSERT INTO public.auth_permission VALUES (73, 'Can add Lotação', 19, 'add_tbllotacao');
INSERT INTO public.auth_permission VALUES (74, 'Can change Lotação', 19, 'change_tbllotacao');
INSERT INTO public.auth_permission VALUES (75, 'Can delete Lotação', 19, 'delete_tbllotacao');
INSERT INTO public.auth_permission VALUES (76, 'Can view Lotação', 19, 'view_tbllotacao');
INSERT INTO public.auth_permission VALUES (77, 'Can add Inconsistência de Lotação', 20, 'add_tbllotacaoinconsistencia');
INSERT INTO public.auth_permission VALUES (78, 'Can change Inconsistência de Lotação', 20, 'change_tbllotacaoinconsistencia');
INSERT INTO public.auth_permission VALUES (79, 'Can delete Inconsistência de Lotação', 20, 'delete_tbllotacaoinconsistencia');
INSERT INTO public.auth_permission VALUES (80, 'Can view Inconsistência de Lotação', 20, 'view_tbllotacaoinconsistencia');
INSERT INTO public.auth_permission VALUES (81, 'Can add JSON Lotação por Órgão', 21, 'add_tbllotacaojsonorgao');
INSERT INTO public.auth_permission VALUES (82, 'Can change JSON Lotação por Órgão', 21, 'change_tbllotacaojsonorgao');
INSERT INTO public.auth_permission VALUES (83, 'Can delete JSON Lotação por Órgão', 21, 'delete_tbllotacaojsonorgao');
INSERT INTO public.auth_permission VALUES (84, 'Can view JSON Lotação por Órgão', 21, 'view_tbllotacaojsonorgao');
INSERT INTO public.auth_permission VALUES (85, 'Can add Versão de Lotação', 22, 'add_tbllotacaoversao');
INSERT INTO public.auth_permission VALUES (86, 'Can change Versão de Lotação', 22, 'change_tbllotacaoversao');
INSERT INTO public.auth_permission VALUES (87, 'Can delete Versão de Lotação', 22, 'delete_tbllotacaoversao');
INSERT INTO public.auth_permission VALUES (88, 'Can view Versão de Lotação', 22, 'view_tbllotacaoversao');
INSERT INTO public.auth_permission VALUES (89, 'Can add JSON Organograma', 23, 'add_tblorganogramajson');
INSERT INTO public.auth_permission VALUES (90, 'Can change JSON Organograma', 23, 'change_tblorganogramajson');
INSERT INTO public.auth_permission VALUES (91, 'Can delete JSON Organograma', 23, 'delete_tblorganogramajson');
INSERT INTO public.auth_permission VALUES (92, 'Can view JSON Organograma', 23, 'view_tblorganogramajson');
INSERT INTO public.auth_permission VALUES (93, 'Can add Versão de Organograma', 24, 'add_tblorganogramaversao');
INSERT INTO public.auth_permission VALUES (94, 'Can change Versão de Organograma', 24, 'change_tblorganogramaversao');
INSERT INTO public.auth_permission VALUES (95, 'Can delete Versão de Organograma', 24, 'delete_tblorganogramaversao');
INSERT INTO public.auth_permission VALUES (96, 'Can view Versão de Organograma', 24, 'view_tblorganogramaversao');
INSERT INTO public.auth_permission VALUES (97, 'Can add Órgão/Unidade', 25, 'add_tblorgaounidade');
INSERT INTO public.auth_permission VALUES (98, 'Can change Órgão/Unidade', 25, 'change_tblorgaounidade');
INSERT INTO public.auth_permission VALUES (99, 'Can delete Órgão/Unidade', 25, 'delete_tblorgaounidade');
INSERT INTO public.auth_permission VALUES (100, 'Can view Órgão/Unidade', 25, 'view_tblorgaounidade');
INSERT INTO public.auth_permission VALUES (101, 'Can add Patriarca', 26, 'add_tblpatriarca');
INSERT INTO public.auth_permission VALUES (102, 'Can change Patriarca', 26, 'change_tblpatriarca');
INSERT INTO public.auth_permission VALUES (103, 'Can delete Patriarca', 26, 'delete_tblpatriarca');
INSERT INTO public.auth_permission VALUES (104, 'Can view Patriarca', 26, 'view_tblpatriarca');
INSERT INTO public.auth_permission VALUES (105, 'Can add Status Carga', 27, 'add_tblstatuscarga');
INSERT INTO public.auth_permission VALUES (106, 'Can change Status Carga', 27, 'change_tblstatuscarga');
INSERT INTO public.auth_permission VALUES (107, 'Can delete Status Carga', 27, 'delete_tblstatuscarga');
INSERT INTO public.auth_permission VALUES (108, 'Can view Status Carga', 27, 'view_tblstatuscarga');
INSERT INTO public.auth_permission VALUES (109, 'Can add Status Progresso', 28, 'add_tblstatusprogresso');
INSERT INTO public.auth_permission VALUES (110, 'Can change Status Progresso', 28, 'change_tblstatusprogresso');
INSERT INTO public.auth_permission VALUES (111, 'Can delete Status Progresso', 28, 'delete_tblstatusprogresso');
INSERT INTO public.auth_permission VALUES (112, 'Can view Status Progresso', 28, 'view_tblstatusprogresso');
INSERT INTO public.auth_permission VALUES (113, 'Can add Status Token Envio Carga', 29, 'add_tblstatustokenenviocarga');
INSERT INTO public.auth_permission VALUES (114, 'Can change Status Token Envio Carga', 29, 'change_tblstatustokenenviocarga');
INSERT INTO public.auth_permission VALUES (115, 'Can delete Status Token Envio Carga', 29, 'delete_tblstatustokenenviocarga');
INSERT INTO public.auth_permission VALUES (116, 'Can view Status Token Envio Carga', 29, 'view_tblstatustokenenviocarga');
INSERT INTO public.auth_permission VALUES (117, 'Can add Tipo Carga', 30, 'add_tbltipocarga');
INSERT INTO public.auth_permission VALUES (118, 'Can change Tipo Carga', 30, 'change_tbltipocarga');
INSERT INTO public.auth_permission VALUES (119, 'Can delete Tipo Carga', 30, 'delete_tbltipocarga');
INSERT INTO public.auth_permission VALUES (120, 'Can view Tipo Carga', 30, 'view_tbltipocarga');
INSERT INTO public.auth_permission VALUES (121, 'Can add Token Envio Carga', 31, 'add_tbltokenenviocarga');
INSERT INTO public.auth_permission VALUES (122, 'Can change Token Envio Carga', 31, 'change_tbltokenenviocarga');
INSERT INTO public.auth_permission VALUES (123, 'Can delete Token Envio Carga', 31, 'delete_tbltokenenviocarga');
INSERT INTO public.auth_permission VALUES (124, 'Can view Token Envio Carga', 31, 'view_tbltokenenviocarga');
INSERT INTO public.auth_permission VALUES (125, 'Can add Permissão de Role', 32, 'add_rolepermission');
INSERT INTO public.auth_permission VALUES (126, 'Can change Permissão de Role', 32, 'change_rolepermission');
INSERT INTO public.auth_permission VALUES (127, 'Can delete Permissão de Role', 32, 'delete_rolepermission');
INSERT INTO public.auth_permission VALUES (128, 'Can view Permissão de Role', 32, 'view_rolepermission');


--
-- TOC entry 5527 (class 0 OID 17942)
-- Dependencies: 272
-- Data for Name: authtoken_token; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.authtoken_token VALUES ('321a7dcee9e7d62c9640dd34762c20fef24ffeeb', '2026-01-23 10:31:33.346063-03', 4);


--
-- TOC entry 5529 (class 0 OID 17959)
-- Dependencies: 274
-- Data for Name: db_service_appclient; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.db_service_appclient VALUES (1, 'portal_gpp_client', 'pbkdf2_sha256$1200000$7WXToFpeRmW81wl0R9FLtD$xSDYXHT/RO0Kaoke71BSSoM+j8lIpIfj4A5IpVAkxSA=', true, 1);
INSERT INTO public.db_service_appclient VALUES (2, 'carga_org_lot_client', 'pbkdf2_sha256$1200000$9Vy7iHSdCt94zh6zD3OYx2$o1T0B9EzLPDT+rHLWDuqntTU4wJv3ENQwaHwwAqe1x8=', true, 2);
INSERT INTO public.db_service_appclient VALUES (3, 'acoes_pngi_client', 'pbkdf2_sha256$1200000$XEmLDIpCgtfcb1A7Oim59a$/4j2WVglFJsp5DtceTXjW7guRBgJL+GAtAAy9yBhhX4=', true, 3);


--
-- TOC entry 5526 (class 0 OID 17916)
-- Dependencies: 271
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.django_admin_log VALUES (1, '2026-01-13 11:45:41.801391-03', '5', 'alexandre.mohamad@seger.es.gov.br', 1, '[{"added": {}}]', 11, 4);
INSERT INTO public.django_admin_log VALUES (2, '2026-01-13 11:53:18.133681-03', '1', 'PortalGPP - Portal GPP', 1, '[{"added": {}}]', 8, 4);
INSERT INTO public.django_admin_log VALUES (3, '2026-01-13 11:53:51.910954-03', '2', 'CargaUnicaOrganogramaLotacao - Carga Única de Organograma e Lotação', 1, '[{"added": {}}]', 8, 4);
INSERT INTO public.django_admin_log VALUES (4, '2026-01-13 14:51:59.693815-03', '1', 'PORTAL - Portal GPP / Usuário do Portal', 1, '[{"added": {}}]', 10, 4);
INSERT INTO public.django_admin_log VALUES (5, '2026-01-13 14:52:25.885507-03', '2', 'CARGA_ORG_LOT - Carga Única de Organograma e Lotação / Gestor Carga Org/Lot', 1, '[{"added": {}}]', 10, 4);
INSERT INTO public.django_admin_log VALUES (6, '2026-01-13 14:53:00.824409-03', '5', 'alexandre.mohamad@seger.es.gov.br', 2, '[{"changed": {"fields": ["Is staff"]}}]', 11, 4);
INSERT INTO public.django_admin_log VALUES (7, '2026-01-13 14:53:30.234479-03', '1', 'alexandre.mohamad@seger.es.gov.br → PORTAL - Portal GPP (PORTAL - Portal GPP / Usuário do Portal)', 1, '[{"added": {}}]', 12, 4);
INSERT INTO public.django_admin_log VALUES (8, '2026-01-13 14:53:39.049169-03', '2', 'alexandre.mohamad@seger.es.gov.br → CARGA_ORG_LOT - Carga Única de Organograma e Lotação (CARGA_ORG_LOT - Carga Única de Organograma e Lotação / Gestor Carga Org/Lot)', 1, '[{"added": {}}]', 12, 4);
INSERT INTO public.django_admin_log VALUES (9, '2026-01-13 14:54:31.785103-03', '1', 'alexandre.mohamad@seger.es.gov.br / CARGA_ORG_LOT / can_upload=true', 1, '[{"added": {}}]', 9, 4);


--
-- TOC entry 5512 (class 0 OID 17773)
-- Dependencies: 257
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.django_content_type VALUES (1, 'admin', 'logentry');
INSERT INTO public.django_content_type VALUES (2, 'auth', 'group');
INSERT INTO public.django_content_type VALUES (3, 'auth', 'permission');
INSERT INTO public.django_content_type VALUES (4, 'contenttypes', 'contenttype');
INSERT INTO public.django_content_type VALUES (5, 'sessions', 'session');
INSERT INTO public.django_content_type VALUES (6, 'authtoken', 'token');
INSERT INTO public.django_content_type VALUES (7, 'authtoken', 'tokenproxy');
INSERT INTO public.django_content_type VALUES (8, 'accounts', 'aplicacao');
INSERT INTO public.django_content_type VALUES (9, 'accounts', 'attribute');
INSERT INTO public.django_content_type VALUES (10, 'accounts', 'role');
INSERT INTO public.django_content_type VALUES (11, 'accounts', 'user');
INSERT INTO public.django_content_type VALUES (12, 'accounts', 'userrole');
INSERT INTO public.django_content_type VALUES (13, 'db_service', 'appclient');
INSERT INTO public.django_content_type VALUES (14, 'acoes_pngi', 'eixo');
INSERT INTO public.django_content_type VALUES (15, 'acoes_pngi', 'situacaoacao');
INSERT INTO public.django_content_type VALUES (16, 'acoes_pngi', 'vigenciapngi');
INSERT INTO public.django_content_type VALUES (17, 'carga_org_lot', 'tblcargapatriarca');
INSERT INTO public.django_content_type VALUES (18, 'carga_org_lot', 'tbldetalhestatuscarga');
INSERT INTO public.django_content_type VALUES (19, 'carga_org_lot', 'tbllotacao');
INSERT INTO public.django_content_type VALUES (20, 'carga_org_lot', 'tbllotacaoinconsistencia');
INSERT INTO public.django_content_type VALUES (21, 'carga_org_lot', 'tbllotacaojsonorgao');
INSERT INTO public.django_content_type VALUES (22, 'carga_org_lot', 'tbllotacaoversao');
INSERT INTO public.django_content_type VALUES (23, 'carga_org_lot', 'tblorganogramajson');
INSERT INTO public.django_content_type VALUES (24, 'carga_org_lot', 'tblorganogramaversao');
INSERT INTO public.django_content_type VALUES (25, 'carga_org_lot', 'tblorgaounidade');
INSERT INTO public.django_content_type VALUES (26, 'carga_org_lot', 'tblpatriarca');
INSERT INTO public.django_content_type VALUES (27, 'carga_org_lot', 'tblstatuscarga');
INSERT INTO public.django_content_type VALUES (28, 'carga_org_lot', 'tblstatusprogresso');
INSERT INTO public.django_content_type VALUES (29, 'carga_org_lot', 'tblstatustokenenviocarga');
INSERT INTO public.django_content_type VALUES (30, 'carga_org_lot', 'tbltipocarga');
INSERT INTO public.django_content_type VALUES (31, 'carga_org_lot', 'tbltokenenviocarga');
INSERT INTO public.django_content_type VALUES (32, 'accounts', 'rolepermission');


--
-- TOC entry 5510 (class 0 OID 17761)
-- Dependencies: 255
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.django_migrations VALUES (101, 'contenttypes', '0001_initial', '2026-01-23 14:56:51.834002-03');
INSERT INTO public.django_migrations VALUES (102, 'contenttypes', '0002_remove_content_type_name', '2026-01-23 14:56:51.837144-03');
INSERT INTO public.django_migrations VALUES (103, 'auth', '0001_initial', '2026-01-23 14:56:51.838341-03');
INSERT INTO public.django_migrations VALUES (104, 'auth', '0002_alter_permission_name_max_length', '2026-01-23 14:56:51.839108-03');
INSERT INTO public.django_migrations VALUES (105, 'auth', '0003_alter_user_email_max_length', '2026-01-23 14:56:51.839927-03');
INSERT INTO public.django_migrations VALUES (106, 'auth', '0004_alter_user_username_opts', '2026-01-23 14:56:51.841039-03');
INSERT INTO public.django_migrations VALUES (107, 'auth', '0005_alter_user_last_login_null', '2026-01-23 14:56:51.841651-03');
INSERT INTO public.django_migrations VALUES (108, 'auth', '0006_require_contenttypes_0002', '2026-01-23 14:56:51.84231-03');
INSERT INTO public.django_migrations VALUES (109, 'auth', '0007_alter_validators_add_error_messages', '2026-01-23 14:56:51.842873-03');
INSERT INTO public.django_migrations VALUES (110, 'auth', '0008_alter_user_username_max_length', '2026-01-23 14:56:51.843433-03');
INSERT INTO public.django_migrations VALUES (111, 'auth', '0009_alter_user_last_name_max_length', '2026-01-23 14:56:51.844003-03');
INSERT INTO public.django_migrations VALUES (112, 'auth', '0010_alter_group_name_max_length', '2026-01-23 14:56:51.844922-03');
INSERT INTO public.django_migrations VALUES (113, 'auth', '0011_update_proxy_permissions', '2026-01-23 14:56:51.845668-03');
INSERT INTO public.django_migrations VALUES (114, 'auth', '0012_alter_user_first_name_max_length', '2026-01-23 14:56:51.846359-03');
INSERT INTO public.django_migrations VALUES (115, 'accounts', '0001_initial', '2026-01-23 14:56:51.847025-03');
INSERT INTO public.django_migrations VALUES (117, 'admin', '0001_initial', '2026-01-23 14:56:51.848173-03');
INSERT INTO public.django_migrations VALUES (118, 'admin', '0002_logentry_remove_auto_add', '2026-01-23 14:56:51.848885-03');
INSERT INTO public.django_migrations VALUES (119, 'admin', '0003_logentry_add_action_flag_choices', '2026-01-23 14:56:51.849666-03');
INSERT INTO public.django_migrations VALUES (120, 'authtoken', '0001_initial', '2026-01-23 14:56:51.850265-03');
INSERT INTO public.django_migrations VALUES (121, 'authtoken', '0002_auto_20160226_1747', '2026-01-23 14:56:51.851073-03');
INSERT INTO public.django_migrations VALUES (122, 'authtoken', '0003_tokenproxy', '2026-01-23 14:56:51.851639-03');
INSERT INTO public.django_migrations VALUES (123, 'authtoken', '0004_alter_tokenproxy_options', '2026-01-23 14:56:51.852197-03');
INSERT INTO public.django_migrations VALUES (124, 'db_service', '0001_initial', '2026-01-23 14:56:51.852881-03');
INSERT INTO public.django_migrations VALUES (125, 'sessions', '0001_initial', '2026-01-23 14:56:51.853597-03');
INSERT INTO public.django_migrations VALUES (126, 'accounts', '0002_alter_attribute_aplicacao', '2026-01-26 08:59:30.836752-03');
INSERT INTO public.django_migrations VALUES (127, 'accounts', '0003_alter_role_aplicacao_alter_userrole_aplicacao', '2026-01-26 09:15:53.658434-03');
INSERT INTO public.django_migrations VALUES (128, 'accounts', '0004_alter_attribute_table_alter_role_table_and_more', '2026-01-26 09:23:32.656318-03');
INSERT INTO public.django_migrations VALUES (129, 'db_service', '0002_alter_appclient_aplicacao_alter_appclient_table', '2026-01-26 09:23:32.666431-03');
INSERT INTO public.django_migrations VALUES (133, 'carga_org_lot', '0001_initial', '2026-01-26 11:43:47.873472-03');
INSERT INTO public.django_migrations VALUES (134, 'carga_org_lot', '0002_alter_tblcargapatriarca_options_and_more', '2026-01-26 13:35:32.235138-03');
INSERT INTO public.django_migrations VALUES (135, 'carga_org_lot', '0003_fix_schema_tables', '2026-01-26 14:51:12.027466-03');
INSERT INTO public.django_migrations VALUES (136, 'accounts', '0005_rolepermission', '2026-01-28 14:43:13.800199-03');
INSERT INTO public.django_migrations VALUES (137, 'acoes_pngi', '0001_create_schema', '2026-01-29 09:19:51.281799-03');
INSERT INTO public.django_migrations VALUES (138, 'acoes_pngi', '0002_initial', '2026-01-29 09:19:51.310143-03');
INSERT INTO public.django_migrations VALUES (140, 'acoes_pngi', '0001_initial', '2026-01-29 10:14:03.375216-03');


--
-- TOC entry 5530 (class 0 OID 17979)
-- Dependencies: 275
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.django_session VALUES ('2o72dqzfq1byfya692m2ayhekdoa730p', '.eJxVjMsKwjAQRf8laynJpJNMXAr9jjB5kaJWMM1K_Pe20IVuz7nnfoTnvlbfW377OYmrQHH5ZYHjPS-H4BhffVnbcKI2TE-eH7dz8FdVbnVPXLEJnE6BlLRO2hIVodPaQTLjaCUGACQVcsn7qdGZFJJJQMCqSC7iuwEkyzM4:1vj0BD:zs15SJ8iIpFPxAFuT4vwNRYc-PoW8H9Jlk_gEGTP9G8', '2026-01-23 16:17:19.05615-03');
INSERT INTO public.django_session VALUES ('ad9avsuyyronvc454bug2iwqhaqcvzr1', '.eJxVjMsKgkAYRt9l1iFzcZwZdyYiQWRY--F3LiiZgqNtonfPwEVuz_nO90YalrnVS3CT7ixKEUeHf9aAebjhJ8CYcRnmEG0oRMUTuv64DXZVC6FdE-WFpYrZRhIsFBbeEMkVY4raJI4F5g2lXJLGebeeJsxJwmViqaRAPAa_noKZu5fT09g7nWd1memqLvW5uqOU7m2WV8VNXy_lCaXs8wWsGkW0:1vlWa8:SF3SqzGNq4adKKoatRkYj5FMgsb_D8tfYc7ilvFePcg', '2026-01-30 15:17:28.12698-03');
INSERT INTO public.django_session VALUES ('z57po5yy57ru5hqvrs40vuwzi85t6ndt', '.eJxVjMsKwjAQRf8laynJpJNMXAr9jjB5kaJWMM1K_Pe20IVuz7nnfoTnvlbfW377OYmrQHH5ZYHjPS-H4BhffVnbcKI2TE-eH7dz8FdVbnVPXLEJnE6BlLRO2hIVodPaQTLjaCUGACQVcsn7qdGZFJJJQMCqSC7iuwEkyzM4:1vgNe1:orrjgqA7St-XIkXu98r7QQyFg2HTvJ6qjGpt56XG61c', '2026-01-16 10:44:13.014045-03');
INSERT INTO public.django_session VALUES ('f24wvci6a3x8zp1so7tlwjkub7f9h0vw', '.eJxVjMsKwjAQRf8laynJpJNMXAr9jjB5kaJWMM1K_Pe20IVuz7nnfoTnvlbfW377OYmrQHH5ZYHjPS-H4BhffVnbcKI2TE-eH7dz8FdVbnVPXLEJnE6BlLRO2hIVodPaQTLjaCUGACQVcsn7qdGZFJJJQMCqSC7iuwEkyzM4:1vhnxX:NnKwg8z7TQPiGNQeQ-pAsUoVvACKBmCuF-GAY_JUOc4', '2026-01-20 09:02:15.070895-03');
INSERT INTO public.django_session VALUES ('twp2xrt3tlfw1475akcbnk4eaibcgk08', '.eJxVjMsKwjAQRf8laynJpJNMXAr9jjB5kaJWMM1K_Pe20IVuz7nnfoTnvlbfW377OYmrQHH5ZYHjPS-H4BhffVnbcKI2TE-eH7dz8FdVbnVPXLEJnE6BlLRO2hIVodPaQTLjaCUGACQVcsn7qdGZFJJJQMCqSC7iuwEkyzM4:1viFDm:50vcLANu8eZiqtW-FMBzO8YdZsQtU4CbNhvFfnxCotQ', '2026-01-21 14:08:50.954857-03');


--
-- TOC entry 5508 (class 0 OID 17738)
-- Dependencies: 253
-- Data for Name: tblaplicacao; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.tblaplicacao VALUES (1, 'PORTAL', 'Portal GPP', 'http://127.0.0.1:8000/portal/', false);
INSERT INTO public.tblaplicacao VALUES (2, 'CARGA_ORG_LOT', 'Carga Única de Organograma e Lotação', 'http://127.0.0.1:8000/carga_org_lot/', true);
INSERT INTO public.tblaplicacao VALUES (3, 'ACOES_PNGI', 'Ações PNGI', 'http://127.0.0.1:8000/acoes-pngi/', true);


--
-- TOC entry 5478 (class 0 OID 16893)
-- Dependencies: 223
-- Data for Name: tblclassificacaousuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.tblclassificacaousuario VALUES (1, 'Gestor Portal');
INSERT INTO public.tblclassificacaousuario VALUES (2, 'Gestor Aplicação');
INSERT INTO public.tblclassificacaousuario VALUES (3, 'Usuário Nível Básico');
INSERT INTO public.tblclassificacaousuario VALUES (4, 'Usuário Nível Intermediário');
INSERT INTO public.tblclassificacaousuario VALUES (5, 'Usuário Nível Avançado');


--
-- TOC entry 5476 (class 0 OID 16879)
-- Dependencies: 221
-- Data for Name: tblstatususuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.tblstatususuario VALUES (1, 'Ativo');
INSERT INTO public.tblstatususuario VALUES (2, 'Inativo');
INSERT INTO public.tblstatususuario VALUES (3, 'Necessita Validação');


--
-- TOC entry 5477 (class 0 OID 16886)
-- Dependencies: 222
-- Data for Name: tbltipousuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.tbltipousuario VALUES (1, 'Interno');
INSERT INTO public.tbltipousuario VALUES (2, 'Externo');


--
-- TOC entry 5480 (class 0 OID 16901)
-- Dependencies: 225
-- Data for Name: tblusuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.tblusuario VALUES (4, '', 'acoesgpp@seger.es.gov.br', 'pbkdf2_sha256$1200000$W2Y60oVRgqbaKbKAHgV9gy$UOa1xOHfLuLvpiAvIv8IWx/zzKPWEzKBXd2wKuqObuY=', 1, 1, 1, '2026-01-13 11:21:35.417706-03', NULL, NULL, NULL, true, true, true, '2026-01-13 11:22:15.922483-03', NULL);
INSERT INTO public.tblusuario VALUES (5, 'Alexandre Wanick Mohamad', 'alexandre.mohamad@seger.es.gov.br', 'pbkdf2_sha256$1200000$7T6S056t0uJiM4yA96hRV8$xvB2YWQMEMgGrkA/C8Qe9FxyIvk5JadphpahMKmbjm8=', 1, 1, 1, '2026-01-13 11:45:41.338314-03', NULL, NULL, NULL, true, false, false, '2026-01-28 16:45:29.185171-03', NULL);


--
-- TOC entry 5532 (class 0 OID 17993)
-- Dependencies: 277
-- Data for Name: tblusuario_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5534 (class 0 OID 18015)
-- Dependencies: 279
-- Data for Name: tblusuario_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5622 (class 0 OID 0)
-- Dependencies: 280
-- Name: tbleixos_ideixo_seq; Type: SEQUENCE SET; Schema: acoes_pngi; Owner: postgres
--

SELECT pg_catalog.setval('acoes_pngi.tbleixos_ideixo_seq', 9, true);


--
-- TOC entry 5623 (class 0 OID 0)
-- Dependencies: 282
-- Name: tblsituacaoacao_idsituacaoacao_seq; Type: SEQUENCE SET; Schema: acoes_pngi; Owner: postgres
--

SELECT pg_catalog.setval('acoes_pngi.tblsituacaoacao_idsituacaoacao_seq', 11, true);


--
-- TOC entry 5624 (class 0 OID 0)
-- Dependencies: 284
-- Name: tblvigenciapngi_idvigenciapngi_seq; Type: SEQUENCE SET; Schema: acoes_pngi; Owner: postgres
--

SELECT pg_catalog.setval('acoes_pngi.tblvigenciapngi_idvigenciapngi_seq', 5, true);


--
-- TOC entry 5625 (class 0 OID 0)
-- Dependencies: 234
-- Name: tblcargapatriarca_idcargapatriarca_seq; Type: SEQUENCE SET; Schema: carga_org_lot; Owner: postgres
--

SELECT pg_catalog.setval('carga_org_lot.tblcargapatriarca_idcargapatriarca_seq', 1, false);


--
-- TOC entry 5626 (class 0 OID 0)
-- Dependencies: 236
-- Name: tbldetalhestatuscarga_iddetalhestatuscarga_seq; Type: SEQUENCE SET; Schema: carga_org_lot; Owner: postgres
--

SELECT pg_catalog.setval('carga_org_lot.tbldetalhestatuscarga_iddetalhestatuscarga_seq', 1, false);


--
-- TOC entry 5627 (class 0 OID 0)
-- Dependencies: 246
-- Name: tbllotacao_idlotacao_seq; Type: SEQUENCE SET; Schema: carga_org_lot; Owner: postgres
--

SELECT pg_catalog.setval('carga_org_lot.tbllotacao_idlotacao_seq', 1, false);


--
-- TOC entry 5628 (class 0 OID 0)
-- Dependencies: 250
-- Name: tbllotacaoinconsistencia_idinconsistencia_seq; Type: SEQUENCE SET; Schema: carga_org_lot; Owner: postgres
--

SELECT pg_catalog.setval('carga_org_lot.tbllotacaoinconsistencia_idinconsistencia_seq', 1, false);


--
-- TOC entry 5629 (class 0 OID 0)
-- Dependencies: 248
-- Name: tbllotacaojsonorgao_idlotacaojsonorgao_seq; Type: SEQUENCE SET; Schema: carga_org_lot; Owner: postgres
--

SELECT pg_catalog.setval('carga_org_lot.tbllotacaojsonorgao_idlotacaojsonorgao_seq', 1, false);


--
-- TOC entry 5630 (class 0 OID 0)
-- Dependencies: 244
-- Name: tbllotacaoversao_idlotacaoversao_seq; Type: SEQUENCE SET; Schema: carga_org_lot; Owner: postgres
--

SELECT pg_catalog.setval('carga_org_lot.tbllotacaoversao_idlotacaoversao_seq', 1, false);


--
-- TOC entry 5631 (class 0 OID 0)
-- Dependencies: 242
-- Name: tblorganogramajson_idorganogramajson_seq; Type: SEQUENCE SET; Schema: carga_org_lot; Owner: postgres
--

SELECT pg_catalog.setval('carga_org_lot.tblorganogramajson_idorganogramajson_seq', 1, false);


--
-- TOC entry 5632 (class 0 OID 0)
-- Dependencies: 238
-- Name: tblorganogramaversao_idorganogramaversao_seq; Type: SEQUENCE SET; Schema: carga_org_lot; Owner: postgres
--

SELECT pg_catalog.setval('carga_org_lot.tblorganogramaversao_idorganogramaversao_seq', 1, false);


--
-- TOC entry 5633 (class 0 OID 0)
-- Dependencies: 240
-- Name: tblorgaounidade_idorgaounidade_seq; Type: SEQUENCE SET; Schema: carga_org_lot; Owner: postgres
--

SELECT pg_catalog.setval('carga_org_lot.tblorgaounidade_idorgaounidade_seq', 1, false);


--
-- TOC entry 5634 (class 0 OID 0)
-- Dependencies: 227
-- Name: tblpatriarca_idpatriarca_seq; Type: SEQUENCE SET; Schema: carga_org_lot; Owner: postgres
--

SELECT pg_catalog.setval('carga_org_lot.tblpatriarca_idpatriarca_seq', 1, false);


--
-- TOC entry 5635 (class 0 OID 0)
-- Dependencies: 230
-- Name: tbltokenenviocarga_idtokenenviocarga_seq; Type: SEQUENCE SET; Schema: carga_org_lot; Owner: postgres
--

SELECT pg_catalog.setval('carga_org_lot.tbltokenenviocarga_idtokenenviocarga_seq', 1, false);


--
-- TOC entry 5636 (class 0 OID 0)
-- Dependencies: 266
-- Name: accounts_attribute_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_attribute_id_seq', 1, true);


--
-- TOC entry 5637 (class 0 OID 0)
-- Dependencies: 264
-- Name: accounts_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_role_id_seq', 10, true);


--
-- TOC entry 5638 (class 0 OID 0)
-- Dependencies: 286
-- Name: accounts_rolepermission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_rolepermission_id_seq', 39, true);


--
-- TOC entry 5639 (class 0 OID 0)
-- Dependencies: 268
-- Name: accounts_userrole_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_userrole_id_seq', 7, true);


--
-- TOC entry 5640 (class 0 OID 0)
-- Dependencies: 260
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- TOC entry 5641 (class 0 OID 0)
-- Dependencies: 262
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- TOC entry 5642 (class 0 OID 0)
-- Dependencies: 258
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 128, true);


--
-- TOC entry 5643 (class 0 OID 0)
-- Dependencies: 273
-- Name: db_service_appclient_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.db_service_appclient_id_seq', 3, true);


--
-- TOC entry 5644 (class 0 OID 0)
-- Dependencies: 270
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 9, true);


--
-- TOC entry 5645 (class 0 OID 0)
-- Dependencies: 256
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 32, true);


--
-- TOC entry 5646 (class 0 OID 0)
-- Dependencies: 254
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 140, true);


--
-- TOC entry 5647 (class 0 OID 0)
-- Dependencies: 252
-- Name: tblaplicacao_idapplication_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tblaplicacao_idapplication_seq', 6, true);


--
-- TOC entry 5648 (class 0 OID 0)
-- Dependencies: 276
-- Name: tblusuario_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tblusuario_groups_id_seq', 1, false);


--
-- TOC entry 5649 (class 0 OID 0)
-- Dependencies: 224
-- Name: tblusuario_idusuario_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tblusuario_idusuario_seq', 5, true);


--
-- TOC entry 5650 (class 0 OID 0)
-- Dependencies: 278
-- Name: tblusuario_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tblusuario_user_permissions_id_seq', 1, false);


--
-- TOC entry 5253 (class 2606 OID 18052)
-- Name: tbleixos tbleixos_pkey; Type: CONSTRAINT; Schema: acoes_pngi; Owner: postgres
--

ALTER TABLE ONLY acoes_pngi.tbleixos
    ADD CONSTRAINT tbleixos_pkey PRIMARY KEY (ideixo);


--
-- TOC entry 5255 (class 2606 OID 18054)
-- Name: tbleixos tbleixos_stralias_key; Type: CONSTRAINT; Schema: acoes_pngi; Owner: postgres
--

ALTER TABLE ONLY acoes_pngi.tbleixos
    ADD CONSTRAINT tbleixos_stralias_key UNIQUE (stralias);


--
-- TOC entry 5258 (class 2606 OID 18063)
-- Name: tblsituacaoacao tblsituacaoacao_pkey; Type: CONSTRAINT; Schema: acoes_pngi; Owner: postgres
--

ALTER TABLE ONLY acoes_pngi.tblsituacaoacao
    ADD CONSTRAINT tblsituacaoacao_pkey PRIMARY KEY (idsituacaoacao);


--
-- TOC entry 5260 (class 2606 OID 18065)
-- Name: tblsituacaoacao tblsituacaoacao_strdescricaosituacao_key; Type: CONSTRAINT; Schema: acoes_pngi; Owner: postgres
--

ALTER TABLE ONLY acoes_pngi.tblsituacaoacao
    ADD CONSTRAINT tblsituacaoacao_strdescricaosituacao_key UNIQUE (strdescricaosituacao);


--
-- TOC entry 5264 (class 2606 OID 18080)
-- Name: tblvigenciapngi tblvigenciapngi_pkey; Type: CONSTRAINT; Schema: acoes_pngi; Owner: postgres
--

ALTER TABLE ONLY acoes_pngi.tblvigenciapngi
    ADD CONSTRAINT tblvigenciapngi_pkey PRIMARY KEY (idvigenciapngi);


--
-- TOC entry 5139 (class 2606 OID 17052)
-- Name: tblcargapatriarca tblcargapatriarca_pkey; Type: CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblcargapatriarca
    ADD CONSTRAINT tblcargapatriarca_pkey PRIMARY KEY (idcargapatriarca);


--
-- TOC entry 5145 (class 2606 OID 17087)
-- Name: tbldetalhestatuscarga tbldetalhestatuscarga_pkey; Type: CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbldetalhestatuscarga
    ADD CONSTRAINT tbldetalhestatuscarga_pkey PRIMARY KEY (iddetalhestatuscarga);


--
-- TOC entry 5167 (class 2606 OID 17240)
-- Name: tbllotacao tbllotacao_pkey; Type: CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbllotacao
    ADD CONSTRAINT tbllotacao_pkey PRIMARY KEY (idlotacao);


--
-- TOC entry 5174 (class 2606 OID 17333)
-- Name: tbllotacaoinconsistencia tbllotacaoinconsistencia_pkey; Type: CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbllotacaoinconsistencia
    ADD CONSTRAINT tbllotacaoinconsistencia_pkey PRIMARY KEY (idinconsistencia);


--
-- TOC entry 5170 (class 2606 OID 17295)
-- Name: tbllotacaojsonorgao tbllotacaojsonorgao_pkey; Type: CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbllotacaojsonorgao
    ADD CONSTRAINT tbllotacaojsonorgao_pkey PRIMARY KEY (idlotacaojsonorgao);


--
-- TOC entry 5162 (class 2606 OID 17209)
-- Name: tbllotacaoversao tbllotacaoversao_pkey; Type: CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbllotacaoversao
    ADD CONSTRAINT tbllotacaoversao_pkey PRIMARY KEY (idlotacaoversao);


--
-- TOC entry 5157 (class 2606 OID 17184)
-- Name: tblorganogramajson tblorganogramajson_pkey; Type: CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblorganogramajson
    ADD CONSTRAINT tblorganogramajson_pkey PRIMARY KEY (idorganogramajson);


--
-- TOC entry 5148 (class 2606 OID 17118)
-- Name: tblorganogramaversao tblorganogramaversao_pkey; Type: CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblorganogramaversao
    ADD CONSTRAINT tblorganogramaversao_pkey PRIMARY KEY (idorganogramaversao);


--
-- TOC entry 5153 (class 2606 OID 17140)
-- Name: tblorgaounidade tblorgaounidade_pkey; Type: CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblorgaounidade
    ADD CONSTRAINT tblorgaounidade_pkey PRIMARY KEY (idorgaounidade);


--
-- TOC entry 5124 (class 2606 OID 16966)
-- Name: tblpatriarca tblpatriarca_pkey; Type: CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblpatriarca
    ADD CONSTRAINT tblpatriarca_pkey PRIMARY KEY (idpatriarca);


--
-- TOC entry 5137 (class 2606 OID 17036)
-- Name: tblstatuscarga tblstatuscarga_pkey; Type: CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblstatuscarga
    ADD CONSTRAINT tblstatuscarga_pkey PRIMARY KEY (idstatuscarga);


--
-- TOC entry 5119 (class 2606 OID 16951)
-- Name: tblstatusprogresso tblstatusprogresso_pkey; Type: CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblstatusprogresso
    ADD CONSTRAINT tblstatusprogresso_pkey PRIMARY KEY (idstatusprogresso);


--
-- TOC entry 5130 (class 2606 OID 16995)
-- Name: tblstatustokenenviocarga tblstatustokenenviocarga_pkey; Type: CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblstatustokenenviocarga
    ADD CONSTRAINT tblstatustokenenviocarga_pkey PRIMARY KEY (idstatustokenenviocarga);


--
-- TOC entry 5135 (class 2606 OID 17028)
-- Name: tbltipocarga tbltipocarga_pkey; Type: CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbltipocarga
    ADD CONSTRAINT tbltipocarga_pkey PRIMARY KEY (idtipocarga);


--
-- TOC entry 5133 (class 2606 OID 17010)
-- Name: tbltokenenviocarga tbltokenenviocarga_pkey; Type: CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbltokenenviocarga
    ADD CONSTRAINT tbltokenenviocarga_pkey PRIMARY KEY (idtokenenviocarga);


--
-- TOC entry 5172 (class 2606 OID 17297)
-- Name: tbllotacaojsonorgao uq_lotjson_versao_org; Type: CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbllotacaojsonorgao
    ADD CONSTRAINT uq_lotjson_versao_org UNIQUE (idlotacaoversao, idorgaolotacao);


--
-- TOC entry 5155 (class 2606 OID 17142)
-- Name: tblorgaounidade uq_orgao_versao_sigla; Type: CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblorgaounidade
    ADD CONSTRAINT uq_orgao_versao_sigla UNIQUE (idorganogramaversao, strsigla);


--
-- TOC entry 5126 (class 2606 OID 16968)
-- Name: tblpatriarca uq_patriarca_idexterno; Type: CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblpatriarca
    ADD CONSTRAINT uq_patriarca_idexterno UNIQUE (idexternopatriarca);


--
-- TOC entry 5128 (class 2606 OID 16970)
-- Name: tblpatriarca uq_patriarca_sigla; Type: CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblpatriarca
    ADD CONSTRAINT uq_patriarca_sigla UNIQUE (strsiglapatriarca);


--
-- TOC entry 5208 (class 2606 OID 17862)
-- Name: accounts_attribute accounts_attribute_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_attribute
    ADD CONSTRAINT accounts_attribute_pkey PRIMARY KEY (id);


--
-- TOC entry 5210 (class 2606 OID 17882)
-- Name: accounts_attribute accounts_attribute_user_id_aplicacao_id_key_67c2d83c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_attribute
    ADD CONSTRAINT accounts_attribute_user_id_aplicacao_id_key_67c2d83c_uniq UNIQUE (user_id, aplicacao_id, key);


--
-- TOC entry 5203 (class 2606 OID 17874)
-- Name: accounts_role accounts_role_aplicacao_id_codigoperfil_474ffdb6_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_role
    ADD CONSTRAINT accounts_role_aplicacao_id_codigoperfil_474ffdb6_uniq UNIQUE (aplicacao_id, codigoperfil);


--
-- TOC entry 5205 (class 2606 OID 17852)
-- Name: accounts_role accounts_role_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_role
    ADD CONSTRAINT accounts_role_pkey PRIMARY KEY (id);


--
-- TOC entry 5267 (class 2606 OID 58157)
-- Name: accounts_rolepermission accounts_rolepermission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_rolepermission
    ADD CONSTRAINT accounts_rolepermission_pkey PRIMARY KEY (id);


--
-- TOC entry 5270 (class 2606 OID 58159)
-- Name: accounts_rolepermission accounts_rolepermission_role_id_permission_id_f150b115_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_rolepermission
    ADD CONSTRAINT accounts_rolepermission_role_id_permission_id_f150b115_uniq UNIQUE (role_id, permission_id);


--
-- TOC entry 5214 (class 2606 OID 17872)
-- Name: accounts_userrole accounts_userrole_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_userrole
    ADD CONSTRAINT accounts_userrole_pkey PRIMARY KEY (id);


--
-- TOC entry 5217 (class 2606 OID 17896)
-- Name: accounts_userrole accounts_userrole_user_id_aplicacao_id_role_id_26c338bf_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_userrole
    ADD CONSTRAINT accounts_userrole_user_id_aplicacao_id_role_id_26c338bf_uniq UNIQUE (user_id, aplicacao_id, role_id);


--
-- TOC entry 5192 (class 2606 OID 17838)
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- TOC entry 5197 (class 2606 OID 17823)
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- TOC entry 5200 (class 2606 OID 17812)
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 5194 (class 2606 OID 17801)
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- TOC entry 5187 (class 2606 OID 17814)
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- TOC entry 5189 (class 2606 OID 17793)
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- TOC entry 5225 (class 2606 OID 17949)
-- Name: authtoken_token authtoken_token_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_pkey PRIMARY KEY (key);


--
-- TOC entry 5227 (class 2606 OID 17951)
-- Name: authtoken_token authtoken_token_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_key UNIQUE (user_id);


--
-- TOC entry 5229 (class 2606 OID 17972)
-- Name: db_service_appclient db_service_appclient_aplicacao_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.db_service_appclient
    ADD CONSTRAINT db_service_appclient_aplicacao_id_key UNIQUE (aplicacao_id);


--
-- TOC entry 5232 (class 2606 OID 17970)
-- Name: db_service_appclient db_service_appclient_client_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.db_service_appclient
    ADD CONSTRAINT db_service_appclient_client_id_key UNIQUE (client_id);


--
-- TOC entry 5234 (class 2606 OID 17968)
-- Name: db_service_appclient db_service_appclient_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.db_service_appclient
    ADD CONSTRAINT db_service_appclient_pkey PRIMARY KEY (id);


--
-- TOC entry 5221 (class 2606 OID 17929)
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- TOC entry 5182 (class 2606 OID 17783)
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- TOC entry 5184 (class 2606 OID 17781)
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- TOC entry 5180 (class 2606 OID 17771)
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- TOC entry 5237 (class 2606 OID 17988)
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- TOC entry 5176 (class 2606 OID 17750)
-- Name: tblaplicacao tblaplicacao_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblaplicacao
    ADD CONSTRAINT tblaplicacao_code_key UNIQUE (codigointerno);


--
-- TOC entry 5178 (class 2606 OID 17748)
-- Name: tblaplicacao tblaplicacao_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblaplicacao
    ADD CONSTRAINT tblaplicacao_pkey PRIMARY KEY (idaplicacao);


--
-- TOC entry 5113 (class 2606 OID 16899)
-- Name: tblclassificacaousuario tblclassificacaousuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblclassificacaousuario
    ADD CONSTRAINT tblclassificacaousuario_pkey PRIMARY KEY (idclassificacaousuario);


--
-- TOC entry 5109 (class 2606 OID 16885)
-- Name: tblstatususuario tblstatususuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblstatususuario
    ADD CONSTRAINT tblstatususuario_pkey PRIMARY KEY (idstatususuario);


--
-- TOC entry 5111 (class 2606 OID 16892)
-- Name: tbltipousuario tbltipousuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbltipousuario
    ADD CONSTRAINT tbltipousuario_pkey PRIMARY KEY (idtipousuario);


--
-- TOC entry 5242 (class 2606 OID 18001)
-- Name: tblusuario_groups tblusuario_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario_groups
    ADD CONSTRAINT tblusuario_groups_pkey PRIMARY KEY (id);


--
-- TOC entry 5244 (class 2606 OID 18003)
-- Name: tblusuario_groups tblusuario_groups_user_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario_groups
    ADD CONSTRAINT tblusuario_groups_user_id_group_id_key UNIQUE (user_id, group_id);


--
-- TOC entry 5115 (class 2606 OID 16917)
-- Name: tblusuario tblusuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario
    ADD CONSTRAINT tblusuario_pkey PRIMARY KEY (idusuario);


--
-- TOC entry 5117 (class 2606 OID 16919)
-- Name: tblusuario tblusuario_stremail_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario
    ADD CONSTRAINT tblusuario_stremail_key UNIQUE (stremail);


--
-- TOC entry 5248 (class 2606 OID 18023)
-- Name: tblusuario_user_permissions tblusuario_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario_user_permissions
    ADD CONSTRAINT tblusuario_user_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 5250 (class 2606 OID 18025)
-- Name: tblusuario_user_permissions tblusuario_user_permissions_user_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario_user_permissions
    ADD CONSTRAINT tblusuario_user_permissions_user_id_permission_id_key UNIQUE (user_id, permission_id);


--
-- TOC entry 5251 (class 1259 OID 18081)
-- Name: idx_eixos_alias; Type: INDEX; Schema: acoes_pngi; Owner: postgres
--

CREATE INDEX idx_eixos_alias ON acoes_pngi.tbleixos USING btree (stralias);


--
-- TOC entry 5256 (class 1259 OID 18082)
-- Name: idx_situacao_descricao; Type: INDEX; Schema: acoes_pngi; Owner: postgres
--

CREATE INDEX idx_situacao_descricao ON acoes_pngi.tblsituacaoacao USING btree (strdescricaosituacao);


--
-- TOC entry 5261 (class 1259 OID 18083)
-- Name: idx_vigencia_ativa; Type: INDEX; Schema: acoes_pngi; Owner: postgres
--

CREATE INDEX idx_vigencia_ativa ON acoes_pngi.tblvigenciapngi USING btree (isvigenciaativa);


--
-- TOC entry 5262 (class 1259 OID 18084)
-- Name: idx_vigencia_datas; Type: INDEX; Schema: acoes_pngi; Owner: postgres
--

CREATE INDEX idx_vigencia_datas ON acoes_pngi.tblvigenciapngi USING btree (datiniciovigencia, datfinalvigencia);


--
-- TOC entry 5141 (class 1259 OID 17098)
-- Name: idx_detstatus_carga; Type: INDEX; Schema: carga_org_lot; Owner: postgres
--

CREATE INDEX idx_detstatus_carga ON carga_org_lot.tbldetalhestatuscarga USING btree (idcargapatriarca);


--
-- TOC entry 5142 (class 1259 OID 17100)
-- Name: idx_detstatus_data; Type: INDEX; Schema: carga_org_lot; Owner: postgres
--

CREATE INDEX idx_detstatus_data ON carga_org_lot.tbldetalhestatuscarga USING btree (datregistro);


--
-- TOC entry 5143 (class 1259 OID 17099)
-- Name: idx_detstatus_status; Type: INDEX; Schema: carga_org_lot; Owner: postgres
--

CREATE INDEX idx_detstatus_status ON carga_org_lot.tbldetalhestatuscarga USING btree (idstatuscarga);


--
-- TOC entry 5163 (class 1259 OID 17277)
-- Name: idx_lotacao_cpf; Type: INDEX; Schema: carga_org_lot; Owner: postgres
--

CREATE INDEX idx_lotacao_cpf ON carga_org_lot.tbllotacao USING btree (strcpf);


--
-- TOC entry 5164 (class 1259 OID 17278)
-- Name: idx_lotacao_org; Type: INDEX; Schema: carga_org_lot; Owner: postgres
--

CREATE INDEX idx_lotacao_org ON carga_org_lot.tbllotacao USING btree (idorgaolotacao);


--
-- TOC entry 5165 (class 1259 OID 17276)
-- Name: idx_lotacao_versao; Type: INDEX; Schema: carga_org_lot; Owner: postgres
--

CREATE INDEX idx_lotacao_versao ON carga_org_lot.tbllotacao USING btree (idlotacaoversao);


--
-- TOC entry 5168 (class 1259 OID 17318)
-- Name: idx_lotjson_orgversao; Type: INDEX; Schema: carga_org_lot; Owner: postgres
--

CREATE INDEX idx_lotjson_orgversao ON carga_org_lot.tbllotacaojsonorgao USING btree (idorganogramaversao);


--
-- TOC entry 5159 (class 1259 OID 17221)
-- Name: idx_lotvers_orgvers; Type: INDEX; Schema: carga_org_lot; Owner: postgres
--

CREATE INDEX idx_lotvers_orgvers ON carga_org_lot.tbllotacaoversao USING btree (idorganogramaversao);


--
-- TOC entry 5160 (class 1259 OID 17220)
-- Name: idx_lotvers_patriarca; Type: INDEX; Schema: carga_org_lot; Owner: postgres
--

CREATE INDEX idx_lotvers_patriarca ON carga_org_lot.tbllotacaoversao USING btree (idpatriarca);


--
-- TOC entry 5149 (class 1259 OID 17170)
-- Name: idx_orgao_numero; Type: INDEX; Schema: carga_org_lot; Owner: postgres
--

CREATE INDEX idx_orgao_numero ON carga_org_lot.tblorgaounidade USING btree (strnumerohierarquia);


--
-- TOC entry 5150 (class 1259 OID 17169)
-- Name: idx_orgao_pai; Type: INDEX; Schema: carga_org_lot; Owner: postgres
--

CREATE INDEX idx_orgao_pai ON carga_org_lot.tblorgaounidade USING btree (idorgaounidadepai);


--
-- TOC entry 5151 (class 1259 OID 17168)
-- Name: idx_orgao_versao; Type: INDEX; Schema: carga_org_lot; Owner: postgres
--

CREATE INDEX idx_orgao_versao ON carga_org_lot.tblorgaounidade USING btree (idorganogramaversao);


--
-- TOC entry 5146 (class 1259 OID 17124)
-- Name: idx_orgvers_patriarca; Type: INDEX; Schema: carga_org_lot; Owner: postgres
--

CREATE INDEX idx_orgvers_patriarca ON carga_org_lot.tblorganogramaversao USING btree (idpatriarca);


--
-- TOC entry 5120 (class 1259 OID 16987)
-- Name: idx_patriarca_idexterno; Type: INDEX; Schema: carga_org_lot; Owner: postgres
--

CREATE INDEX idx_patriarca_idexterno ON carga_org_lot.tblpatriarca USING btree (idexternopatriarca);


--
-- TOC entry 5121 (class 1259 OID 16986)
-- Name: idx_patriarca_nome; Type: INDEX; Schema: carga_org_lot; Owner: postgres
--

CREATE INDEX idx_patriarca_nome ON carga_org_lot.tblpatriarca USING btree (strnome);


--
-- TOC entry 5122 (class 1259 OID 16988)
-- Name: idx_patriarca_sigla; Type: INDEX; Schema: carga_org_lot; Owner: postgres
--

CREATE INDEX idx_patriarca_sigla ON carga_org_lot.tblpatriarca USING btree (strsiglapatriarca);


--
-- TOC entry 5131 (class 1259 OID 17021)
-- Name: idx_token_patriarca; Type: INDEX; Schema: carga_org_lot; Owner: postgres
--

CREATE INDEX idx_token_patriarca ON carga_org_lot.tbltokenenviocarga USING btree (idpatriarca);


--
-- TOC entry 5140 (class 1259 OID 17073)
-- Name: uq_carga_patriarca_token_tipo; Type: INDEX; Schema: carga_org_lot; Owner: postgres
--

CREATE UNIQUE INDEX uq_carga_patriarca_token_tipo ON carga_org_lot.tblcargapatriarca USING btree (idpatriarca, idtokenenviocarga, idtipocarga);


--
-- TOC entry 5158 (class 1259 OID 17190)
-- Name: uq_orgjson_versao; Type: INDEX; Schema: carga_org_lot; Owner: postgres
--

CREATE UNIQUE INDEX uq_orgjson_versao ON carga_org_lot.tblorganogramajson USING btree (idorganogramaversao);


--
-- TOC entry 5206 (class 1259 OID 17893)
-- Name: accounts_attribute_aplicacao_id_5139e1c1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_attribute_aplicacao_id_5139e1c1 ON public.accounts_attribute USING btree (aplicacao_id);


--
-- TOC entry 5211 (class 1259 OID 17894)
-- Name: accounts_attribute_user_id_e505d190; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_attribute_user_id_e505d190 ON public.accounts_attribute USING btree (user_id);


--
-- TOC entry 5201 (class 1259 OID 17880)
-- Name: accounts_role_aplicacao_id_180a9da1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_role_aplicacao_id_180a9da1 ON public.accounts_role USING btree (aplicacao_id);


--
-- TOC entry 5265 (class 1259 OID 58170)
-- Name: accounts_rolepermission_permission_id_f7e3fe09; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_rolepermission_permission_id_f7e3fe09 ON public.accounts_rolepermission USING btree (permission_id);


--
-- TOC entry 5268 (class 1259 OID 58171)
-- Name: accounts_rolepermission_role_id_db688956; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_rolepermission_role_id_db688956 ON public.accounts_rolepermission USING btree (role_id);


--
-- TOC entry 5212 (class 1259 OID 17912)
-- Name: accounts_userrole_aplicacao_id_e9e35b67; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_userrole_aplicacao_id_e9e35b67 ON public.accounts_userrole USING btree (aplicacao_id);


--
-- TOC entry 5215 (class 1259 OID 17913)
-- Name: accounts_userrole_role_id_9448d870; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_userrole_role_id_9448d870 ON public.accounts_userrole USING btree (role_id);


--
-- TOC entry 5218 (class 1259 OID 17914)
-- Name: accounts_userrole_user_id_eba3c754; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_userrole_user_id_eba3c754 ON public.accounts_userrole USING btree (user_id);


--
-- TOC entry 5190 (class 1259 OID 17839)
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- TOC entry 5195 (class 1259 OID 17834)
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- TOC entry 5198 (class 1259 OID 17835)
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- TOC entry 5185 (class 1259 OID 17820)
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- TOC entry 5223 (class 1259 OID 17957)
-- Name: authtoken_token_key_10f0b77e_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX authtoken_token_key_10f0b77e_like ON public.authtoken_token USING btree (key varchar_pattern_ops);


--
-- TOC entry 5230 (class 1259 OID 17978)
-- Name: db_service_appclient_client_id_a6545fb2_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX db_service_appclient_client_id_a6545fb2_like ON public.db_service_appclient USING btree (client_id varchar_pattern_ops);


--
-- TOC entry 5219 (class 1259 OID 17940)
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- TOC entry 5222 (class 1259 OID 17941)
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- TOC entry 5235 (class 1259 OID 17990)
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- TOC entry 5238 (class 1259 OID 17989)
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- TOC entry 5239 (class 1259 OID 18037)
-- Name: idx_tblusuario_groups_group; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_tblusuario_groups_group ON public.tblusuario_groups USING btree (group_id);


--
-- TOC entry 5240 (class 1259 OID 18036)
-- Name: idx_tblusuario_groups_user; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_tblusuario_groups_user ON public.tblusuario_groups USING btree (user_id);


--
-- TOC entry 5245 (class 1259 OID 18039)
-- Name: idx_tblusuario_perms_perm; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_tblusuario_perms_perm ON public.tblusuario_user_permissions USING btree (permission_id);


--
-- TOC entry 5246 (class 1259 OID 18038)
-- Name: idx_tblusuario_perms_user; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_tblusuario_perms_user ON public.tblusuario_user_permissions USING btree (user_id);


--
-- TOC entry 5327 (class 2620 OID 18086)
-- Name: tbleixos update_tbleixos_updated_at; Type: TRIGGER; Schema: acoes_pngi; Owner: postgres
--

CREATE TRIGGER update_tbleixos_updated_at BEFORE UPDATE ON acoes_pngi.tbleixos FOR EACH ROW EXECUTE FUNCTION acoes_pngi.update_updated_at_column();


--
-- TOC entry 5328 (class 2620 OID 18088)
-- Name: tblvigenciapngi update_tblvigenciapngi_updated_at; Type: TRIGGER; Schema: acoes_pngi; Owner: postgres
--

CREATE TRIGGER update_tblvigenciapngi_updated_at BEFORE UPDATE ON acoes_pngi.tblvigenciapngi FOR EACH ROW EXECUTE FUNCTION acoes_pngi.update_updated_at_column();


--
-- TOC entry 5281 (class 2606 OID 17053)
-- Name: tblcargapatriarca tblcargapatriarca_idpatriarca_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblcargapatriarca
    ADD CONSTRAINT tblcargapatriarca_idpatriarca_fkey FOREIGN KEY (idpatriarca) REFERENCES carga_org_lot.tblpatriarca(idpatriarca);


--
-- TOC entry 5282 (class 2606 OID 17063)
-- Name: tblcargapatriarca tblcargapatriarca_idstatuscarga_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblcargapatriarca
    ADD CONSTRAINT tblcargapatriarca_idstatuscarga_fkey FOREIGN KEY (idstatuscarga) REFERENCES carga_org_lot.tblstatuscarga(idstatuscarga);


--
-- TOC entry 5283 (class 2606 OID 17068)
-- Name: tblcargapatriarca tblcargapatriarca_idtipocarga_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblcargapatriarca
    ADD CONSTRAINT tblcargapatriarca_idtipocarga_fkey FOREIGN KEY (idtipocarga) REFERENCES carga_org_lot.tbltipocarga(idtipocarga);


--
-- TOC entry 5284 (class 2606 OID 17058)
-- Name: tblcargapatriarca tblcargapatriarca_idtokenenviocarga_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblcargapatriarca
    ADD CONSTRAINT tblcargapatriarca_idtokenenviocarga_fkey FOREIGN KEY (idtokenenviocarga) REFERENCES carga_org_lot.tbltokenenviocarga(idtokenenviocarga);


--
-- TOC entry 5285 (class 2606 OID 17088)
-- Name: tbldetalhestatuscarga tbldetalhestatuscarga_idcargapatriarca_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbldetalhestatuscarga
    ADD CONSTRAINT tbldetalhestatuscarga_idcargapatriarca_fkey FOREIGN KEY (idcargapatriarca) REFERENCES carga_org_lot.tblcargapatriarca(idcargapatriarca) ON DELETE CASCADE;


--
-- TOC entry 5286 (class 2606 OID 17093)
-- Name: tbldetalhestatuscarga tbldetalhestatuscarga_idstatuscarga_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbldetalhestatuscarga
    ADD CONSTRAINT tbldetalhestatuscarga_idstatuscarga_fkey FOREIGN KEY (idstatuscarga) REFERENCES carga_org_lot.tblstatuscarga(idstatuscarga);


--
-- TOC entry 5296 (class 2606 OID 17241)
-- Name: tbllotacao tbllotacao_idlotacaoversao_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbllotacao
    ADD CONSTRAINT tbllotacao_idlotacaoversao_fkey FOREIGN KEY (idlotacaoversao) REFERENCES carga_org_lot.tbllotacaoversao(idlotacaoversao) ON DELETE CASCADE;


--
-- TOC entry 5297 (class 2606 OID 17246)
-- Name: tbllotacao tbllotacao_idorganogramaversao_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbllotacao
    ADD CONSTRAINT tbllotacao_idorganogramaversao_fkey FOREIGN KEY (idorganogramaversao) REFERENCES carga_org_lot.tblorganogramaversao(idorganogramaversao);


--
-- TOC entry 5298 (class 2606 OID 17256)
-- Name: tbllotacao tbllotacao_idorgaolotacao_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbllotacao
    ADD CONSTRAINT tbllotacao_idorgaolotacao_fkey FOREIGN KEY (idorgaolotacao) REFERENCES carga_org_lot.tblorgaounidade(idorgaounidade);


--
-- TOC entry 5299 (class 2606 OID 17251)
-- Name: tbllotacao tbllotacao_idpatriarca_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbllotacao
    ADD CONSTRAINT tbllotacao_idpatriarca_fkey FOREIGN KEY (idpatriarca) REFERENCES carga_org_lot.tblpatriarca(idpatriarca);


--
-- TOC entry 5300 (class 2606 OID 17261)
-- Name: tbllotacao tbllotacao_idunidadelotacao_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbllotacao
    ADD CONSTRAINT tbllotacao_idunidadelotacao_fkey FOREIGN KEY (idunidadelotacao) REFERENCES carga_org_lot.tblorgaounidade(idorgaounidade);


--
-- TOC entry 5301 (class 2606 OID 17271)
-- Name: tbllotacao tbllotacao_idusuarioalteracao_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbllotacao
    ADD CONSTRAINT tbllotacao_idusuarioalteracao_fkey FOREIGN KEY (idusuarioalteracao) REFERENCES public.tblusuario(idusuario);


--
-- TOC entry 5302 (class 2606 OID 17266)
-- Name: tbllotacao tbllotacao_idusuariocriacao_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbllotacao
    ADD CONSTRAINT tbllotacao_idusuariocriacao_fkey FOREIGN KEY (idusuariocriacao) REFERENCES public.tblusuario(idusuario);


--
-- TOC entry 5307 (class 2606 OID 17334)
-- Name: tbllotacaoinconsistencia tbllotacaoinconsistencia_idlotacao_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbllotacaoinconsistencia
    ADD CONSTRAINT tbllotacaoinconsistencia_idlotacao_fkey FOREIGN KEY (idlotacao) REFERENCES carga_org_lot.tbllotacao(idlotacao) ON DELETE CASCADE;


--
-- TOC entry 5303 (class 2606 OID 17298)
-- Name: tbllotacaojsonorgao tbllotacaojsonorgao_idlotacaoversao_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbllotacaojsonorgao
    ADD CONSTRAINT tbllotacaojsonorgao_idlotacaoversao_fkey FOREIGN KEY (idlotacaoversao) REFERENCES carga_org_lot.tbllotacaoversao(idlotacaoversao) ON DELETE CASCADE;


--
-- TOC entry 5304 (class 2606 OID 17303)
-- Name: tbllotacaojsonorgao tbllotacaojsonorgao_idorganogramaversao_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbllotacaojsonorgao
    ADD CONSTRAINT tbllotacaojsonorgao_idorganogramaversao_fkey FOREIGN KEY (idorganogramaversao) REFERENCES carga_org_lot.tblorganogramaversao(idorganogramaversao);


--
-- TOC entry 5305 (class 2606 OID 17313)
-- Name: tbllotacaojsonorgao tbllotacaojsonorgao_idorgaolotacao_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbllotacaojsonorgao
    ADD CONSTRAINT tbllotacaojsonorgao_idorgaolotacao_fkey FOREIGN KEY (idorgaolotacao) REFERENCES carga_org_lot.tblorgaounidade(idorgaounidade);


--
-- TOC entry 5306 (class 2606 OID 17308)
-- Name: tbllotacaojsonorgao tbllotacaojsonorgao_idpatriarca_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbllotacaojsonorgao
    ADD CONSTRAINT tbllotacaojsonorgao_idpatriarca_fkey FOREIGN KEY (idpatriarca) REFERENCES carga_org_lot.tblpatriarca(idpatriarca);


--
-- TOC entry 5294 (class 2606 OID 17215)
-- Name: tbllotacaoversao tbllotacaoversao_idorganogramaversao_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbllotacaoversao
    ADD CONSTRAINT tbllotacaoversao_idorganogramaversao_fkey FOREIGN KEY (idorganogramaversao) REFERENCES carga_org_lot.tblorganogramaversao(idorganogramaversao);


--
-- TOC entry 5295 (class 2606 OID 17210)
-- Name: tbllotacaoversao tbllotacaoversao_idpatriarca_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbllotacaoversao
    ADD CONSTRAINT tbllotacaoversao_idpatriarca_fkey FOREIGN KEY (idpatriarca) REFERENCES carga_org_lot.tblpatriarca(idpatriarca);


--
-- TOC entry 5293 (class 2606 OID 17185)
-- Name: tblorganogramajson tblorganogramajson_idorganogramaversao_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblorganogramajson
    ADD CONSTRAINT tblorganogramajson_idorganogramaversao_fkey FOREIGN KEY (idorganogramaversao) REFERENCES carga_org_lot.tblorganogramaversao(idorganogramaversao) ON DELETE CASCADE;


--
-- TOC entry 5287 (class 2606 OID 17119)
-- Name: tblorganogramaversao tblorganogramaversao_idpatriarca_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblorganogramaversao
    ADD CONSTRAINT tblorganogramaversao_idpatriarca_fkey FOREIGN KEY (idpatriarca) REFERENCES carga_org_lot.tblpatriarca(idpatriarca);


--
-- TOC entry 5288 (class 2606 OID 17143)
-- Name: tblorgaounidade tblorgaounidade_idorganogramaversao_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblorgaounidade
    ADD CONSTRAINT tblorgaounidade_idorganogramaversao_fkey FOREIGN KEY (idorganogramaversao) REFERENCES carga_org_lot.tblorganogramaversao(idorganogramaversao) ON DELETE RESTRICT;


--
-- TOC entry 5289 (class 2606 OID 17153)
-- Name: tblorgaounidade tblorgaounidade_idorgaounidadepai_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblorgaounidade
    ADD CONSTRAINT tblorgaounidade_idorgaounidadepai_fkey FOREIGN KEY (idorgaounidadepai) REFERENCES carga_org_lot.tblorgaounidade(idorgaounidade);


--
-- TOC entry 5290 (class 2606 OID 17148)
-- Name: tblorgaounidade tblorgaounidade_idpatriarca_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblorgaounidade
    ADD CONSTRAINT tblorgaounidade_idpatriarca_fkey FOREIGN KEY (idpatriarca) REFERENCES carga_org_lot.tblpatriarca(idpatriarca) ON DELETE RESTRICT;


--
-- TOC entry 5291 (class 2606 OID 17163)
-- Name: tblorgaounidade tblorgaounidade_idusuarioalteracao_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblorgaounidade
    ADD CONSTRAINT tblorgaounidade_idusuarioalteracao_fkey FOREIGN KEY (idusuarioalteracao) REFERENCES public.tblusuario(idusuario);


--
-- TOC entry 5292 (class 2606 OID 17158)
-- Name: tblorgaounidade tblorgaounidade_idusuariocriacao_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblorgaounidade
    ADD CONSTRAINT tblorgaounidade_idusuariocriacao_fkey FOREIGN KEY (idusuariocriacao) REFERENCES public.tblusuario(idusuario);


--
-- TOC entry 5276 (class 2606 OID 16971)
-- Name: tblpatriarca tblpatriarca_idstatusprogresso_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblpatriarca
    ADD CONSTRAINT tblpatriarca_idstatusprogresso_fkey FOREIGN KEY (idstatusprogresso) REFERENCES carga_org_lot.tblstatusprogresso(idstatusprogresso);


--
-- TOC entry 5277 (class 2606 OID 16981)
-- Name: tblpatriarca tblpatriarca_idusuarioalteracao_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblpatriarca
    ADD CONSTRAINT tblpatriarca_idusuarioalteracao_fkey FOREIGN KEY (idusuarioalteracao) REFERENCES public.tblusuario(idusuario);


--
-- TOC entry 5278 (class 2606 OID 16976)
-- Name: tblpatriarca tblpatriarca_idusuariocriacao_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tblpatriarca
    ADD CONSTRAINT tblpatriarca_idusuariocriacao_fkey FOREIGN KEY (idusuariocriacao) REFERENCES public.tblusuario(idusuario);


--
-- TOC entry 5279 (class 2606 OID 17011)
-- Name: tbltokenenviocarga tbltokenenviocarga_idpatriarca_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbltokenenviocarga
    ADD CONSTRAINT tbltokenenviocarga_idpatriarca_fkey FOREIGN KEY (idpatriarca) REFERENCES carga_org_lot.tblpatriarca(idpatriarca);


--
-- TOC entry 5280 (class 2606 OID 17016)
-- Name: tbltokenenviocarga tbltokenenviocarga_idstatustokenenviocarga_fkey; Type: FK CONSTRAINT; Schema: carga_org_lot; Owner: postgres
--

ALTER TABLE ONLY carga_org_lot.tbltokenenviocarga
    ADD CONSTRAINT tbltokenenviocarga_idstatustokenenviocarga_fkey FOREIGN KEY (idstatustokenenviocarga) REFERENCES carga_org_lot.tblstatustokenenviocarga(idstatustokenenviocarga);


--
-- TOC entry 5312 (class 2606 OID 17883)
-- Name: accounts_attribute accounts_attribute_aplicacao_id_5139e1c1_fk_tblaplica; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_attribute
    ADD CONSTRAINT accounts_attribute_aplicacao_id_5139e1c1_fk_tblaplica FOREIGN KEY (aplicacao_id) REFERENCES public.tblaplicacao(idaplicacao) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5313 (class 2606 OID 17888)
-- Name: accounts_attribute accounts_attribute_user_id_e505d190_fk_tblusuario_idusuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_attribute
    ADD CONSTRAINT accounts_attribute_user_id_e505d190_fk_tblusuario_idusuario FOREIGN KEY (user_id) REFERENCES public.tblusuario(idusuario) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5311 (class 2606 OID 28266)
-- Name: accounts_role accounts_role_aplicacao_id_180a9da1_fk_tblaplicacao_idaplicacao; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_role
    ADD CONSTRAINT accounts_role_aplicacao_id_180a9da1_fk_tblaplicacao_idaplicacao FOREIGN KEY (aplicacao_id) REFERENCES public.tblaplicacao(idaplicacao) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5325 (class 2606 OID 58160)
-- Name: accounts_rolepermission accounts_rolepermiss_permission_id_f7e3fe09_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_rolepermission
    ADD CONSTRAINT accounts_rolepermiss_permission_id_f7e3fe09_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5326 (class 2606 OID 58165)
-- Name: accounts_rolepermission accounts_rolepermission_role_id_db688956_fk_accounts_role_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_rolepermission
    ADD CONSTRAINT accounts_rolepermission_role_id_db688956_fk_accounts_role_id FOREIGN KEY (role_id) REFERENCES public.accounts_role(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5314 (class 2606 OID 28271)
-- Name: accounts_userrole accounts_userrole_aplicacao_id_e9e35b67_fk_tblaplica; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_userrole
    ADD CONSTRAINT accounts_userrole_aplicacao_id_e9e35b67_fk_tblaplica FOREIGN KEY (aplicacao_id) REFERENCES public.tblaplicacao(idaplicacao) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5315 (class 2606 OID 17902)
-- Name: accounts_userrole accounts_userrole_role_id_9448d870_fk_accounts_role_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_userrole
    ADD CONSTRAINT accounts_userrole_role_id_9448d870_fk_accounts_role_id FOREIGN KEY (role_id) REFERENCES public.accounts_role(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5316 (class 2606 OID 17907)
-- Name: accounts_userrole accounts_userrole_user_id_eba3c754_fk_tblusuario_idusuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_userrole
    ADD CONSTRAINT accounts_userrole_user_id_eba3c754_fk_tblusuario_idusuario FOREIGN KEY (user_id) REFERENCES public.tblusuario(idusuario) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5309 (class 2606 OID 17829)
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5310 (class 2606 OID 17824)
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5308 (class 2606 OID 17815)
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5319 (class 2606 OID 17952)
-- Name: authtoken_token authtoken_token_user_id_35299eff_fk_tblusuario_idusuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_35299eff_fk_tblusuario_idusuario FOREIGN KEY (user_id) REFERENCES public.tblusuario(idusuario) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5320 (class 2606 OID 17973)
-- Name: db_service_appclient db_service_appclient_aplicacao_id_bd7a7a76_fk_tblaplica; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.db_service_appclient
    ADD CONSTRAINT db_service_appclient_aplicacao_id_bd7a7a76_fk_tblaplica FOREIGN KEY (aplicacao_id) REFERENCES public.tblaplicacao(idaplicacao) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5317 (class 2606 OID 17930)
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5318 (class 2606 OID 17935)
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_tblusuario_idusuario; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_tblusuario_idusuario FOREIGN KEY (user_id) REFERENCES public.tblusuario(idusuario) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5321 (class 2606 OID 18009)
-- Name: tblusuario_groups tblusuario_groups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario_groups
    ADD CONSTRAINT tblusuario_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.auth_group(id) ON DELETE CASCADE;


--
-- TOC entry 5322 (class 2606 OID 18004)
-- Name: tblusuario_groups tblusuario_groups_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario_groups
    ADD CONSTRAINT tblusuario_groups_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.tblusuario(idusuario) ON DELETE CASCADE;


--
-- TOC entry 5271 (class 2606 OID 16930)
-- Name: tblusuario tblusuario_idclassificacaousuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario
    ADD CONSTRAINT tblusuario_idclassificacaousuario_fkey FOREIGN KEY (idclassificacaousuario) REFERENCES public.tblclassificacaousuario(idclassificacaousuario);


--
-- TOC entry 5272 (class 2606 OID 16920)
-- Name: tblusuario tblusuario_idstatususuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario
    ADD CONSTRAINT tblusuario_idstatususuario_fkey FOREIGN KEY (idstatususuario) REFERENCES public.tblstatususuario(idstatususuario);


--
-- TOC entry 5273 (class 2606 OID 16925)
-- Name: tblusuario tblusuario_idtipousuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario
    ADD CONSTRAINT tblusuario_idtipousuario_fkey FOREIGN KEY (idtipousuario) REFERENCES public.tbltipousuario(idtipousuario);


--
-- TOC entry 5274 (class 2606 OID 16940)
-- Name: tblusuario tblusuario_idusuarioalteracao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario
    ADD CONSTRAINT tblusuario_idusuarioalteracao_fkey FOREIGN KEY (idusuarioalteracao) REFERENCES public.tblusuario(idusuario);


--
-- TOC entry 5275 (class 2606 OID 16935)
-- Name: tblusuario tblusuario_idusuariocriacao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario
    ADD CONSTRAINT tblusuario_idusuariocriacao_fkey FOREIGN KEY (idusuariocriacao) REFERENCES public.tblusuario(idusuario);


--
-- TOC entry 5323 (class 2606 OID 18031)
-- Name: tblusuario_user_permissions tblusuario_user_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario_user_permissions
    ADD CONSTRAINT tblusuario_user_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) ON DELETE CASCADE;


--
-- TOC entry 5324 (class 2606 OID 18026)
-- Name: tblusuario_user_permissions tblusuario_user_permissions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tblusuario_user_permissions
    ADD CONSTRAINT tblusuario_user_permissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.tblusuario(idusuario) ON DELETE CASCADE;


--
-- TOC entry 5549 (class 0 OID 0)
-- Dependencies: 6
-- Name: SCHEMA acoes_pngi; Type: ACL; Schema: -; Owner: postgres
--

GRANT USAGE ON SCHEMA acoes_pngi TO acoes_pngi_app;


--
-- TOC entry 5550 (class 0 OID 0)
-- Dependencies: 7
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT USAGE ON SCHEMA public TO portal_app;
GRANT USAGE ON SCHEMA public TO acoes_pngi_app;


--
-- TOC entry 5551 (class 0 OID 0)
-- Dependencies: 288
-- Name: FUNCTION acoes_pngi_create_eixo(p_alias character varying, p_descricao character varying); Type: ACL; Schema: acoes_pngi; Owner: postgres
--

GRANT ALL ON FUNCTION acoes_pngi.acoes_pngi_create_eixo(p_alias character varying, p_descricao character varying) TO acoes_pngi_app;


--
-- TOC entry 5552 (class 0 OID 0)
-- Dependencies: 302
-- Name: FUNCTION update_updated_at_column(); Type: ACL; Schema: acoes_pngi; Owner: postgres
--

GRANT ALL ON FUNCTION acoes_pngi.update_updated_at_column() TO acoes_pngi_app;


--
-- TOC entry 5553 (class 0 OID 0)
-- Dependencies: 306
-- Name: FUNCTION sp_get_timeline_carga(p_idcargapatriarca bigint); Type: ACL; Schema: carga_org_lot; Owner: postgres
--

GRANT ALL ON FUNCTION carga_org_lot.sp_get_timeline_carga(p_idcargapatriarca bigint) TO carga_org_lot_app;


--
-- TOC entry 5554 (class 0 OID 0)
-- Dependencies: 307
-- Name: FUNCTION sp_insert_carga_patriarca(p_idpatriarca bigint, p_idtokenenviocarga bigint, p_idstatuscarga integer, p_idtipocarga integer, p_strmensagemretorno text); Type: ACL; Schema: carga_org_lot; Owner: postgres
--

GRANT ALL ON FUNCTION carga_org_lot.sp_insert_carga_patriarca(p_idpatriarca bigint, p_idtokenenviocarga bigint, p_idstatuscarga integer, p_idtipocarga integer, p_strmensagemretorno text) TO carga_org_lot_app;


--
-- TOC entry 5555 (class 0 OID 0)
-- Dependencies: 312
-- Name: FUNCTION sp_insert_detalhe_status_carga(p_idcargapatriarca bigint, p_idstatuscarga integer, p_strmensagem text); Type: ACL; Schema: carga_org_lot; Owner: postgres
--

GRANT ALL ON FUNCTION carga_org_lot.sp_insert_detalhe_status_carga(p_idcargapatriarca bigint, p_idstatuscarga integer, p_strmensagem text) TO carga_org_lot_app;


--
-- TOC entry 5556 (class 0 OID 0)
-- Dependencies: 308
-- Name: FUNCTION sp_insert_lotacao(p_idlotacaoversao bigint, p_idpatriarca bigint, p_idorgaolotacao bigint, p_idunidadelotacao bigint, p_strcpf text, p_strcargooriginal text, p_strcargonormalizado text, p_flgvalido boolean, p_strerrosvalidacao text, p_datreferencia date, p_idusuariocriacao bigint); Type: ACL; Schema: carga_org_lot; Owner: postgres
--

GRANT ALL ON FUNCTION carga_org_lot.sp_insert_lotacao(p_idlotacaoversao bigint, p_idpatriarca bigint, p_idorgaolotacao bigint, p_idunidadelotacao bigint, p_strcpf text, p_strcargooriginal text, p_strcargonormalizado text, p_flgvalido boolean, p_strerrosvalidacao text, p_datreferencia date, p_idusuariocriacao bigint) TO carga_org_lot_app;


--
-- TOC entry 5557 (class 0 OID 0)
-- Dependencies: 313
-- Name: FUNCTION sp_insert_lotacao_inconsistencia(p_idlotacao bigint, p_strtipo text, p_strdetalhe text); Type: ACL; Schema: carga_org_lot; Owner: postgres
--

GRANT ALL ON FUNCTION carga_org_lot.sp_insert_lotacao_inconsistencia(p_idlotacao bigint, p_strtipo text, p_strdetalhe text) TO carga_org_lot_app;


--
-- TOC entry 5558 (class 0 OID 0)
-- Dependencies: 309
-- Name: FUNCTION sp_insert_lotacao_json_orgao(p_idlotacaoversao bigint, p_idorganogramaversao bigint, p_idpatriarca bigint, p_idorgaolotacao bigint, p_jsconteudo jsonb); Type: ACL; Schema: carga_org_lot; Owner: postgres
--

GRANT ALL ON FUNCTION carga_org_lot.sp_insert_lotacao_json_orgao(p_idlotacaoversao bigint, p_idorganogramaversao bigint, p_idpatriarca bigint, p_idorgaolotacao bigint, p_jsconteudo jsonb) TO carga_org_lot_app;


--
-- TOC entry 5559 (class 0 OID 0)
-- Dependencies: 318
-- Name: FUNCTION sp_insert_lotacao_versao(p_idpatriarca bigint, p_strorigem text, p_strtipoarquivooriginal text, p_strnomearquivooriginal text); Type: ACL; Schema: carga_org_lot; Owner: postgres
--

GRANT ALL ON FUNCTION carga_org_lot.sp_insert_lotacao_versao(p_idpatriarca bigint, p_strorigem text, p_strtipoarquivooriginal text, p_strnomearquivooriginal text) TO carga_org_lot_app;


--
-- TOC entry 5560 (class 0 OID 0)
-- Dependencies: 310
-- Name: FUNCTION sp_insert_organograma_json(p_idorganogramaversao bigint, p_jsconteudo jsonb); Type: ACL; Schema: carga_org_lot; Owner: postgres
--

GRANT ALL ON FUNCTION carga_org_lot.sp_insert_organograma_json(p_idorganogramaversao bigint, p_jsconteudo jsonb) TO carga_org_lot_app;


--
-- TOC entry 5561 (class 0 OID 0)
-- Dependencies: 311
-- Name: FUNCTION sp_insert_patriarca(p_idexternopatriarca uuid, p_strsiglapatriarca text, p_strnome text, p_idstatusprogresso integer, p_idusuariocriacao bigint); Type: ACL; Schema: carga_org_lot; Owner: postgres
--

GRANT ALL ON FUNCTION carga_org_lot.sp_insert_patriarca(p_idexternopatriarca uuid, p_strsiglapatriarca text, p_strnome text, p_idstatusprogresso integer, p_idusuariocriacao bigint) TO carga_org_lot_app;


--
-- TOC entry 5562 (class 0 OID 0)
-- Dependencies: 314
-- Name: FUNCTION sp_insert_status_carga(p_idstatuscarga integer, p_strdescricao text, p_flgsucesso integer); Type: ACL; Schema: carga_org_lot; Owner: postgres
--

GRANT ALL ON FUNCTION carga_org_lot.sp_insert_status_carga(p_idstatuscarga integer, p_strdescricao text, p_flgsucesso integer) TO carga_org_lot_app;


--
-- TOC entry 5563 (class 0 OID 0)
-- Dependencies: 315
-- Name: FUNCTION sp_insert_tipo_carga(p_idtipocarga integer, p_strdescricao text); Type: ACL; Schema: carga_org_lot; Owner: postgres
--

GRANT ALL ON FUNCTION carga_org_lot.sp_insert_tipo_carga(p_idtipocarga integer, p_strdescricao text) TO carga_org_lot_app;


--
-- TOC entry 5564 (class 0 OID 0)
-- Dependencies: 316
-- Name: FUNCTION sp_insert_token_envio_carga(p_idpatriarca bigint, p_idstatustokenenviocarga integer, p_strtokenretorno text); Type: ACL; Schema: carga_org_lot; Owner: postgres
--

GRANT ALL ON FUNCTION carga_org_lot.sp_insert_token_envio_carga(p_idpatriarca bigint, p_idstatustokenenviocarga integer, p_strtokenretorno text) TO carga_org_lot_app;


--
-- TOC entry 5565 (class 0 OID 0)
-- Dependencies: 319
-- Name: FUNCTION sp_set_organograma_versao_ativa(p_idpatriarca bigint, p_idorganogramaversao bigint); Type: ACL; Schema: carga_org_lot; Owner: postgres
--

GRANT ALL ON FUNCTION carga_org_lot.sp_set_organograma_versao_ativa(p_idpatriarca bigint, p_idorganogramaversao bigint) TO carga_org_lot_app;


--
-- TOC entry 5566 (class 0 OID 0)
-- Dependencies: 317
-- Name: FUNCTION sp_update_patriarca(p_idpatriarca bigint, p_strnome text, p_idstatusprogresso integer, p_idusuarioalteracao bigint); Type: ACL; Schema: carga_org_lot; Owner: postgres
--

GRANT ALL ON FUNCTION carga_org_lot.sp_update_patriarca(p_idpatriarca bigint, p_strnome text, p_idstatusprogresso integer, p_idusuarioalteracao bigint) TO carga_org_lot_app;


--
-- TOC entry 5568 (class 0 OID 0)
-- Dependencies: 281
-- Name: TABLE tbleixos; Type: ACL; Schema: acoes_pngi; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE acoes_pngi.tbleixos TO acoes_pngi_app;


--
-- TOC entry 5570 (class 0 OID 0)
-- Dependencies: 280
-- Name: SEQUENCE tbleixos_ideixo_seq; Type: ACL; Schema: acoes_pngi; Owner: postgres
--

GRANT ALL ON SEQUENCE acoes_pngi.tbleixos_ideixo_seq TO acoes_pngi_app;


--
-- TOC entry 5572 (class 0 OID 0)
-- Dependencies: 283
-- Name: TABLE tblsituacaoacao; Type: ACL; Schema: acoes_pngi; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE acoes_pngi.tblsituacaoacao TO acoes_pngi_app;


--
-- TOC entry 5574 (class 0 OID 0)
-- Dependencies: 282
-- Name: SEQUENCE tblsituacaoacao_idsituacaoacao_seq; Type: ACL; Schema: acoes_pngi; Owner: postgres
--

GRANT ALL ON SEQUENCE acoes_pngi.tblsituacaoacao_idsituacaoacao_seq TO acoes_pngi_app;


--
-- TOC entry 5576 (class 0 OID 0)
-- Dependencies: 285
-- Name: TABLE tblvigenciapngi; Type: ACL; Schema: acoes_pngi; Owner: postgres
--

GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE acoes_pngi.tblvigenciapngi TO acoes_pngi_app;


--
-- TOC entry 5578 (class 0 OID 0)
-- Dependencies: 284
-- Name: SEQUENCE tblvigenciapngi_idvigenciapngi_seq; Type: ACL; Schema: acoes_pngi; Owner: postgres
--

GRANT ALL ON SEQUENCE acoes_pngi.tblvigenciapngi_idvigenciapngi_seq TO acoes_pngi_app;


--
-- TOC entry 5580 (class 0 OID 0)
-- Dependencies: 234
-- Name: SEQUENCE tblcargapatriarca_idcargapatriarca_seq; Type: ACL; Schema: carga_org_lot; Owner: postgres
--

GRANT ALL ON SEQUENCE carga_org_lot.tblcargapatriarca_idcargapatriarca_seq TO carga_org_lot_app;


--
-- TOC entry 5582 (class 0 OID 0)
-- Dependencies: 236
-- Name: SEQUENCE tbldetalhestatuscarga_iddetalhestatuscarga_seq; Type: ACL; Schema: carga_org_lot; Owner: postgres
--

GRANT ALL ON SEQUENCE carga_org_lot.tbldetalhestatuscarga_iddetalhestatuscarga_seq TO carga_org_lot_app;


--
-- TOC entry 5584 (class 0 OID 0)
-- Dependencies: 246
-- Name: SEQUENCE tbllotacao_idlotacao_seq; Type: ACL; Schema: carga_org_lot; Owner: postgres
--

GRANT ALL ON SEQUENCE carga_org_lot.tbllotacao_idlotacao_seq TO carga_org_lot_app;


--
-- TOC entry 5586 (class 0 OID 0)
-- Dependencies: 250
-- Name: SEQUENCE tbllotacaoinconsistencia_idinconsistencia_seq; Type: ACL; Schema: carga_org_lot; Owner: postgres
--

GRANT ALL ON SEQUENCE carga_org_lot.tbllotacaoinconsistencia_idinconsistencia_seq TO carga_org_lot_app;


--
-- TOC entry 5588 (class 0 OID 0)
-- Dependencies: 248
-- Name: SEQUENCE tbllotacaojsonorgao_idlotacaojsonorgao_seq; Type: ACL; Schema: carga_org_lot; Owner: postgres
--

GRANT ALL ON SEQUENCE carga_org_lot.tbllotacaojsonorgao_idlotacaojsonorgao_seq TO carga_org_lot_app;


--
-- TOC entry 5590 (class 0 OID 0)
-- Dependencies: 244
-- Name: SEQUENCE tbllotacaoversao_idlotacaoversao_seq; Type: ACL; Schema: carga_org_lot; Owner: postgres
--

GRANT ALL ON SEQUENCE carga_org_lot.tbllotacaoversao_idlotacaoversao_seq TO carga_org_lot_app;


--
-- TOC entry 5592 (class 0 OID 0)
-- Dependencies: 242
-- Name: SEQUENCE tblorganogramajson_idorganogramajson_seq; Type: ACL; Schema: carga_org_lot; Owner: postgres
--

GRANT ALL ON SEQUENCE carga_org_lot.tblorganogramajson_idorganogramajson_seq TO carga_org_lot_app;


--
-- TOC entry 5594 (class 0 OID 0)
-- Dependencies: 238
-- Name: SEQUENCE tblorganogramaversao_idorganogramaversao_seq; Type: ACL; Schema: carga_org_lot; Owner: postgres
--

GRANT ALL ON SEQUENCE carga_org_lot.tblorganogramaversao_idorganogramaversao_seq TO carga_org_lot_app;


--
-- TOC entry 5596 (class 0 OID 0)
-- Dependencies: 240
-- Name: SEQUENCE tblorgaounidade_idorgaounidade_seq; Type: ACL; Schema: carga_org_lot; Owner: postgres
--

GRANT ALL ON SEQUENCE carga_org_lot.tblorgaounidade_idorgaounidade_seq TO carga_org_lot_app;


--
-- TOC entry 5598 (class 0 OID 0)
-- Dependencies: 227
-- Name: SEQUENCE tblpatriarca_idpatriarca_seq; Type: ACL; Schema: carga_org_lot; Owner: postgres
--

GRANT ALL ON SEQUENCE carga_org_lot.tblpatriarca_idpatriarca_seq TO carga_org_lot_app;


--
-- TOC entry 5600 (class 0 OID 0)
-- Dependencies: 230
-- Name: SEQUENCE tbltokenenviocarga_idtokenenviocarga_seq; Type: ACL; Schema: carga_org_lot; Owner: postgres
--

GRANT ALL ON SEQUENCE carga_org_lot.tbltokenenviocarga_idtokenenviocarga_seq TO carga_org_lot_app;


--
-- TOC entry 5601 (class 0 OID 0)
-- Dependencies: 267
-- Name: TABLE accounts_attribute; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.accounts_attribute TO portal_app;
GRANT SELECT ON TABLE public.accounts_attribute TO acoes_pngi_app;
GRANT SELECT ON TABLE public.accounts_attribute TO carga_org_lot_app;


--
-- TOC entry 5602 (class 0 OID 0)
-- Dependencies: 265
-- Name: TABLE accounts_role; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.accounts_role TO portal_app;
GRANT SELECT ON TABLE public.accounts_role TO acoes_pngi_app;
GRANT SELECT ON TABLE public.accounts_role TO carga_org_lot_app;


--
-- TOC entry 5603 (class 0 OID 0)
-- Dependencies: 287
-- Name: TABLE accounts_rolepermission; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.accounts_rolepermission TO portal_app;
GRANT SELECT ON TABLE public.accounts_rolepermission TO acoes_pngi_app;
GRANT SELECT ON TABLE public.accounts_rolepermission TO carga_org_lot_app;


--
-- TOC entry 5604 (class 0 OID 0)
-- Dependencies: 269
-- Name: TABLE accounts_userrole; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.accounts_userrole TO portal_app;
GRANT SELECT ON TABLE public.accounts_userrole TO acoes_pngi_app;
GRANT SELECT ON TABLE public.accounts_userrole TO carga_org_lot_app;


--
-- TOC entry 5605 (class 0 OID 0)
-- Dependencies: 261
-- Name: TABLE auth_group; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.auth_group TO portal_app;
GRANT SELECT ON TABLE public.auth_group TO acoes_pngi_app;
GRANT SELECT ON TABLE public.auth_group TO carga_org_lot_app;


--
-- TOC entry 5606 (class 0 OID 0)
-- Dependencies: 263
-- Name: TABLE auth_group_permissions; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.auth_group_permissions TO portal_app;
GRANT SELECT ON TABLE public.auth_group_permissions TO acoes_pngi_app;
GRANT SELECT ON TABLE public.auth_group_permissions TO carga_org_lot_app;


--
-- TOC entry 5607 (class 0 OID 0)
-- Dependencies: 259
-- Name: TABLE auth_permission; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.auth_permission TO portal_app;
GRANT SELECT ON TABLE public.auth_permission TO acoes_pngi_app;
GRANT SELECT ON TABLE public.auth_permission TO carga_org_lot_app;


--
-- TOC entry 5608 (class 0 OID 0)
-- Dependencies: 272
-- Name: TABLE authtoken_token; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.authtoken_token TO portal_app;
GRANT SELECT ON TABLE public.authtoken_token TO acoes_pngi_app;
GRANT SELECT ON TABLE public.authtoken_token TO carga_org_lot_app;


--
-- TOC entry 5609 (class 0 OID 0)
-- Dependencies: 274
-- Name: TABLE db_service_appclient; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.db_service_appclient TO acoes_pngi_app;
GRANT SELECT ON TABLE public.db_service_appclient TO carga_org_lot_app;
GRANT SELECT ON TABLE public.db_service_appclient TO portal_app;


--
-- TOC entry 5610 (class 0 OID 0)
-- Dependencies: 275
-- Name: TABLE django_session; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.django_session TO portal_app;


--
-- TOC entry 5611 (class 0 OID 0)
-- Dependencies: 253
-- Name: TABLE tblaplicacao; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.tblaplicacao TO portal_app;
GRANT SELECT ON TABLE public.tblaplicacao TO acoes_pngi_app;
GRANT SELECT ON TABLE public.tblaplicacao TO carga_org_lot_app;


--
-- TOC entry 5613 (class 0 OID 0)
-- Dependencies: 223
-- Name: TABLE tblclassificacaousuario; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.tblclassificacaousuario TO acoes_pngi_app;
GRANT SELECT ON TABLE public.tblclassificacaousuario TO carga_org_lot_app;


--
-- TOC entry 5614 (class 0 OID 0)
-- Dependencies: 221
-- Name: TABLE tblstatususuario; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.tblstatususuario TO acoes_pngi_app;
GRANT SELECT ON TABLE public.tblstatususuario TO carga_org_lot_app;


--
-- TOC entry 5615 (class 0 OID 0)
-- Dependencies: 222
-- Name: TABLE tbltipousuario; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.tbltipousuario TO acoes_pngi_app;
GRANT SELECT ON TABLE public.tbltipousuario TO carga_org_lot_app;


--
-- TOC entry 5616 (class 0 OID 0)
-- Dependencies: 225
-- Name: TABLE tblusuario; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.tblusuario TO portal_app;
GRANT SELECT ON TABLE public.tblusuario TO acoes_pngi_app;
GRANT SELECT ON TABLE public.tblusuario TO carga_org_lot_app;


--
-- TOC entry 5617 (class 0 OID 0)
-- Dependencies: 277
-- Name: TABLE tblusuario_groups; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.tblusuario_groups TO acoes_pngi_app;
GRANT SELECT ON TABLE public.tblusuario_groups TO carga_org_lot_app;


--
-- TOC entry 5620 (class 0 OID 0)
-- Dependencies: 279
-- Name: TABLE tblusuario_user_permissions; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.tblusuario_user_permissions TO acoes_pngi_app;
GRANT SELECT ON TABLE public.tblusuario_user_permissions TO carga_org_lot_app;


--
-- TOC entry 2252 (class 826 OID 18126)
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: acoes_pngi; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA acoes_pngi GRANT ALL ON FUNCTIONS TO acoes_pngi_app;


--
-- TOC entry 2251 (class 826 OID 18125)
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: acoes_pngi; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA acoes_pngi GRANT ALL ON TABLES TO acoes_pngi_app;


--
-- TOC entry 2254 (class 826 OID 18128)
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: carga_org_lot; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA carga_org_lot GRANT ALL ON FUNCTIONS TO carga_org_lot_app;


--
-- TOC entry 2253 (class 826 OID 18127)
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: carga_org_lot; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA carga_org_lot GRANT ALL ON TABLES TO carga_org_lot_app;


--
-- TOC entry 2255 (class 826 OID 18129)
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT SELECT ON TABLES TO portal_app;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT SELECT ON TABLES TO acoes_pngi_app;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT SELECT ON TABLES TO carga_org_lot_app;


-- Completed on 2026-01-30 11:00:10

--
-- PostgreSQL database dump complete
--

\unrestrict 3hnj753vFqsx3AJikubXIr9D9e77XKYgaVbCH2uthjhYqYRPPxgA2WuQp7Eb2SH

