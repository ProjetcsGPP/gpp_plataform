-- DROP ROLE acoes_pngi_app;

CREATE ROLE acoes_pngi_app WITH 
	NOSUPERUSER
	NOCREATEDB
	NOCREATEROLE
	INHERIT
	LOGIN
	NOREPLICATION
	NOBYPASSRLS
	CONNECTION LIMIT -1;

-- Permissions

GRANT USAGE ON SCHEMA acoes_pngi TO acoes_pngi_app;
GRANT EXECUTE ON FUNCTION acoes_pngi.acoes_pngi_create_eixo(varchar, varchar) TO acoes_pngi_app;
GRANT REFERENCES, TRIGGER, SELECT, DELETE, UPDATE, INSERT, TRUNCATE ON TABLE acoes_pngi.tbleixos TO acoes_pngi_app;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE acoes_pngi.tbleixos_ideixo_seq TO acoes_pngi_app;
GRANT REFERENCES, TRIGGER, SELECT, DELETE, UPDATE, INSERT, TRUNCATE ON TABLE acoes_pngi.tblsituacaoacao TO acoes_pngi_app;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE acoes_pngi.tblsituacaoacao_idsituacaoacao_seq TO acoes_pngi_app;
GRANT REFERENCES, TRIGGER, SELECT, DELETE, UPDATE, INSERT, TRUNCATE ON TABLE acoes_pngi.tblvigenciapngi TO acoes_pngi_app;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE acoes_pngi.tblvigenciapngi_idvigenciapngi_seq TO acoes_pngi_app;
GRANT EXECUTE ON FUNCTION acoes_pngi.update_updated_at_column() TO acoes_pngi_app;
GRANT SELECT ON TABLE public.accounts_attribute TO acoes_pngi_app;
GRANT SELECT ON TABLE public.accounts_role TO acoes_pngi_app;
GRANT SELECT ON TABLE public.accounts_rolepermission TO acoes_pngi_app;
GRANT SELECT ON TABLE public.accounts_userrole TO acoes_pngi_app;
GRANT SELECT ON TABLE public.auth_group TO acoes_pngi_app;
GRANT SELECT ON TABLE public.auth_group_permissions TO acoes_pngi_app;
GRANT SELECT ON TABLE public.auth_permission TO acoes_pngi_app;
GRANT SELECT ON TABLE public.authtoken_token TO acoes_pngi_app;
GRANT SELECT ON TABLE public.db_service_appclient TO acoes_pngi_app;
GRANT USAGE ON SCHEMA public TO acoes_pngi_app;
GRANT SELECT ON TABLE public.tblaplicacao TO acoes_pngi_app;
GRANT SELECT ON TABLE public.tblclassificacaousuario TO acoes_pngi_app;
GRANT SELECT ON TABLE public.tblstatususuario TO acoes_pngi_app;
GRANT SELECT ON TABLE public.tbltipousuario TO acoes_pngi_app;
GRANT SELECT ON TABLE public.tblusuario TO acoes_pngi_app;
GRANT SELECT ON TABLE public.tblusuario_groups TO acoes_pngi_app;
GRANT SELECT ON TABLE public.tblusuario_user_permissions TO acoes_pngi_app;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT SELECT ON TABLES TO acoes_pngi_app;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA acoes_pngi GRANT REFERENCES, TRIGGER, SELECT, DELETE, UPDATE, INSERT, TRUNCATE, MAINTAIN ON TABLES TO acoes_pngi_app;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA acoes_pngi GRANT EXECUTE ON FUNCTIONS TO acoes_pngi_app;

-- DROP ROLE carga_org_lot_app;

CREATE ROLE carga_org_lot_app WITH 
	NOSUPERUSER
	NOCREATEDB
	NOCREATEROLE
	INHERIT
	LOGIN
	NOREPLICATION
	NOBYPASSRLS
	CONNECTION LIMIT -1;

-- Permissions

GRANT EXECUTE ON FUNCTION carga_org_lot.sp_get_timeline_carga(int8) TO carga_org_lot_app;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_insert_carga_patriarca(int8, int8, int4, int4, text) TO carga_org_lot_app;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_insert_detalhe_status_carga(int8, int4, text) TO carga_org_lot_app;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_insert_lotacao(int8, int8, int8, int8, text, text, text, bool, text, date, int8) TO carga_org_lot_app;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_insert_lotacao_inconsistencia(int8, text, text) TO carga_org_lot_app;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_insert_lotacao_json_orgao(int8, int8, int8, int8, jsonb) TO carga_org_lot_app;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_insert_lotacao_versao(int8, text, text, text) TO carga_org_lot_app;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_insert_organograma_json(int8, jsonb) TO carga_org_lot_app;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_insert_patriarca(uuid, text, text, int4, int8) TO carga_org_lot_app;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_insert_status_carga(int4, text, int4) TO carga_org_lot_app;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_insert_tipo_carga(int4, text) TO carga_org_lot_app;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_insert_token_envio_carga(int8, int4, text) TO carga_org_lot_app;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_set_organograma_versao_ativa(int8, int8) TO carga_org_lot_app;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_update_patriarca(int8, text, int4, int8) TO carga_org_lot_app;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE carga_org_lot.tblcargapatriarca_idcargapatriarca_seq TO carga_org_lot_app;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE carga_org_lot.tbldetalhestatuscarga_iddetalhestatuscarga_seq TO carga_org_lot_app;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE carga_org_lot.tbllotacao_idlotacao_seq TO carga_org_lot_app;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE carga_org_lot.tbllotacaoinconsistencia_idinconsistencia_seq TO carga_org_lot_app;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE carga_org_lot.tbllotacaojsonorgao_idlotacaojsonorgao_seq TO carga_org_lot_app;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE carga_org_lot.tbllotacaoversao_idlotacaoversao_seq TO carga_org_lot_app;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE carga_org_lot.tblorganogramajson_idorganogramajson_seq TO carga_org_lot_app;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE carga_org_lot.tblorganogramaversao_idorganogramaversao_seq TO carga_org_lot_app;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE carga_org_lot.tblorgaounidade_idorgaounidade_seq TO carga_org_lot_app;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE carga_org_lot.tblpatriarca_idpatriarca_seq TO carga_org_lot_app;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE carga_org_lot.tbltokenenviocarga_idtokenenviocarga_seq TO carga_org_lot_app;
GRANT SELECT ON TABLE public.accounts_attribute TO carga_org_lot_app;
GRANT SELECT ON TABLE public.accounts_role TO carga_org_lot_app;
GRANT SELECT ON TABLE public.accounts_rolepermission TO carga_org_lot_app;
GRANT SELECT ON TABLE public.accounts_userrole TO carga_org_lot_app;
GRANT SELECT ON TABLE public.auth_group TO carga_org_lot_app;
GRANT SELECT ON TABLE public.auth_group_permissions TO carga_org_lot_app;
GRANT SELECT ON TABLE public.auth_permission TO carga_org_lot_app;
GRANT SELECT ON TABLE public.authtoken_token TO carga_org_lot_app;
GRANT SELECT ON TABLE public.db_service_appclient TO carga_org_lot_app;
GRANT SELECT ON TABLE public.tblaplicacao TO carga_org_lot_app;
GRANT SELECT ON TABLE public.tblclassificacaousuario TO carga_org_lot_app;
GRANT SELECT ON TABLE public.tblstatususuario TO carga_org_lot_app;
GRANT SELECT ON TABLE public.tbltipousuario TO carga_org_lot_app;
GRANT SELECT ON TABLE public.tblusuario TO carga_org_lot_app;
GRANT SELECT ON TABLE public.tblusuario_groups TO carga_org_lot_app;
GRANT SELECT ON TABLE public.tblusuario_user_permissions TO carga_org_lot_app;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA carga_org_lot GRANT REFERENCES, TRIGGER, SELECT, DELETE, UPDATE, INSERT, TRUNCATE, MAINTAIN ON TABLES TO carga_org_lot_app;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT SELECT ON TABLES TO carga_org_lot_app;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA carga_org_lot GRANT EXECUTE ON FUNCTIONS TO carga_org_lot_app;

-- DROP ROLE gpp_connect;

CREATE ROLE gpp_connect WITH 
	NOSUPERUSER
	NOCREATEDB
	NOCREATEROLE
	INHERIT
	LOGIN
	NOREPLICATION
	NOBYPASSRLS
	CONNECTION LIMIT -1;

-- Permissions;

-- DROP ROLE portal_app;

CREATE ROLE portal_app WITH 
	NOSUPERUSER
	NOCREATEDB
	NOCREATEROLE
	INHERIT
	LOGIN
	NOREPLICATION
	NOBYPASSRLS
	CONNECTION LIMIT -1;

-- Permissions

GRANT SELECT, DELETE, UPDATE, INSERT ON TABLE public.accounts_attribute TO portal_app;
GRANT SELECT, DELETE, UPDATE, INSERT ON TABLE public.accounts_role TO portal_app;
GRANT SELECT ON TABLE public.accounts_rolepermission TO portal_app;
GRANT SELECT, DELETE, UPDATE, INSERT ON TABLE public.accounts_userrole TO portal_app;
GRANT SELECT ON TABLE public.auth_group TO portal_app;
GRANT SELECT ON TABLE public.auth_group_permissions TO portal_app;
GRANT SELECT ON TABLE public.auth_permission TO portal_app;
GRANT SELECT ON TABLE public.authtoken_token TO portal_app;
GRANT SELECT ON TABLE public.db_service_appclient TO portal_app;
GRANT SELECT ON TABLE public.django_session TO portal_app;
GRANT USAGE ON SCHEMA public TO portal_app;
GRANT SELECT ON TABLE public.tblaplicacao TO portal_app;
GRANT SELECT, DELETE, UPDATE, INSERT ON TABLE public.tblusuario TO portal_app;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT SELECT ON TABLES TO portal_app;

-- DROP ROLE postgres;

CREATE ROLE postgres WITH 
	SUPERUSER
	CREATEDB
	CREATEROLE
	INHERIT
	LOGIN
	REPLICATION
	BYPASSRLS
	CONNECTION LIMIT -1;

-- Permissions

GRANT USAGE, CREATE ON SCHEMA acoes_pngi TO postgres;
GRANT EXECUTE ON FUNCTION acoes_pngi.acoes_pngi_create_eixo(varchar, varchar) TO postgres WITH GRANT OPTION;
GRANT REFERENCES, TRIGGER, SELECT, DELETE, UPDATE, INSERT, TRUNCATE ON TABLE acoes_pngi.tbleixos TO postgres WITH GRANT OPTION;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE acoes_pngi.tbleixos_ideixo_seq TO postgres;
GRANT REFERENCES, TRIGGER, SELECT, DELETE, UPDATE, INSERT, TRUNCATE ON TABLE acoes_pngi.tblsituacaoacao TO postgres WITH GRANT OPTION;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE acoes_pngi.tblsituacaoacao_idsituacaoacao_seq TO postgres;
GRANT REFERENCES, TRIGGER, SELECT, DELETE, UPDATE, INSERT, TRUNCATE ON TABLE acoes_pngi.tblvigenciapngi TO postgres WITH GRANT OPTION;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE acoes_pngi.tblvigenciapngi_idvigenciapngi_seq TO postgres;
GRANT EXECUTE ON FUNCTION acoes_pngi.update_updated_at_column() TO postgres WITH GRANT OPTION;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_get_timeline_carga(int8) TO postgres WITH GRANT OPTION;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_insert_carga_patriarca(int8, int8, int4, int4, text) TO postgres WITH GRANT OPTION;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_insert_detalhe_status_carga(int8, int4, text) TO postgres WITH GRANT OPTION;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_insert_lotacao(int8, int8, int8, int8, text, text, text, bool, text, date, int8) TO postgres WITH GRANT OPTION;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_insert_lotacao_inconsistencia(int8, text, text) TO postgres WITH GRANT OPTION;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_insert_lotacao_json_orgao(int8, int8, int8, int8, jsonb) TO postgres WITH GRANT OPTION;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_insert_lotacao_versao(int8, text, text, text) TO postgres WITH GRANT OPTION;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_insert_organograma_json(int8, jsonb) TO postgres WITH GRANT OPTION;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_insert_patriarca(uuid, text, text, int4, int8) TO postgres WITH GRANT OPTION;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_insert_status_carga(int4, text, int4) TO postgres WITH GRANT OPTION;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_insert_tipo_carga(int4, text) TO postgres WITH GRANT OPTION;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_insert_token_envio_carga(int8, int4, text) TO postgres WITH GRANT OPTION;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_set_organograma_versao_ativa(int8, int8) TO postgres WITH GRANT OPTION;
GRANT EXECUTE ON FUNCTION carga_org_lot.sp_update_patriarca(int8, text, int4, int8) TO postgres WITH GRANT OPTION;
GRANT REFERENCES, TRIGGER, SELECT, DELETE, UPDATE, INSERT, TRUNCATE ON TABLE carga_org_lot.tblcargapatriarca TO postgres WITH GRANT OPTION;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE carga_org_lot.tblcargapatriarca_idcargapatriarca_seq TO postgres;
GRANT REFERENCES, TRIGGER, SELECT, DELETE, UPDATE, INSERT, TRUNCATE ON TABLE carga_org_lot.tbldetalhestatuscarga TO postgres WITH GRANT OPTION;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE carga_org_lot.tbldetalhestatuscarga_iddetalhestatuscarga_seq TO postgres;
GRANT REFERENCES, TRIGGER, SELECT, DELETE, UPDATE, INSERT, TRUNCATE ON TABLE carga_org_lot.tbllotacao TO postgres WITH GRANT OPTION;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE carga_org_lot.tbllotacao_idlotacao_seq TO postgres;
GRANT REFERENCES, TRIGGER, SELECT, DELETE, UPDATE, INSERT, TRUNCATE ON TABLE carga_org_lot.tbllotacaoinconsistencia TO postgres WITH GRANT OPTION;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE carga_org_lot.tbllotacaoinconsistencia_idinconsistencia_seq TO postgres;
GRANT REFERENCES, TRIGGER, SELECT, DELETE, UPDATE, INSERT, TRUNCATE ON TABLE carga_org_lot.tbllotacaojsonorgao TO postgres WITH GRANT OPTION;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE carga_org_lot.tbllotacaojsonorgao_idlotacaojsonorgao_seq TO postgres;
GRANT REFERENCES, TRIGGER, SELECT, DELETE, UPDATE, INSERT, TRUNCATE ON TABLE carga_org_lot.tbllotacaoversao TO postgres WITH GRANT OPTION;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE carga_org_lot.tbllotacaoversao_idlotacaoversao_seq TO postgres;
GRANT REFERENCES, TRIGGER, SELECT, DELETE, UPDATE, INSERT, TRUNCATE ON TABLE carga_org_lot.tblorganogramajson TO postgres WITH GRANT OPTION;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE carga_org_lot.tblorganogramajson_idorganogramajson_seq TO postgres;
GRANT REFERENCES, TRIGGER, SELECT, DELETE, UPDATE, INSERT, TRUNCATE ON TABLE carga_org_lot.tblorganogramaversao TO postgres WITH GRANT OPTION;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE carga_org_lot.tblorganogramaversao_idorganogramaversao_seq TO postgres;
GRANT REFERENCES, TRIGGER, SELECT, DELETE, UPDATE, INSERT, TRUNCATE ON TABLE carga_org_lot.tblorgaounidade TO postgres WITH GRANT OPTION;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE carga_org_lot.tblorgaounidade_idorgaounidade_seq TO postgres;
GRANT REFERENCES, TRIGGER, SELECT, DELETE, UPDATE, INSERT, TRUNCATE ON TABLE carga_org_lot.tblpatriarca TO postgres WITH GRANT OPTION;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE carga_org_lot.tblpatriarca_idpatriarca_seq TO postgres;
GRANT REFERENCES, TRIGGER, SELECT, DELETE, UPDATE, INSERT, TRUNCATE ON TABLE carga_org_lot.tblstatuscarga TO postgres WITH GRANT OPTION;
GRANT REFERENCES, TRIGGER, SELECT, DELETE, UPDATE, INSERT, TRUNCATE ON TABLE carga_org_lot.tblstatusprogresso TO postgres WITH GRANT OPTION;
GRANT REFERENCES, TRIGGER, SELECT, DELETE, UPDATE, INSERT, TRUNCATE ON TABLE carga_org_lot.tblstatustokenenviocarga TO postgres WITH GRANT OPTION;
GRANT REFERENCES, TRIGGER, SELECT, DELETE, UPDATE, INSERT, TRUNCATE ON TABLE carga_org_lot.tbltipocarga TO postgres WITH GRANT OPTION;
GRANT REFERENCES, TRIGGER, SELECT, DELETE, UPDATE, INSERT, TRUNCATE ON TABLE carga_org_lot.tbltokenenviocarga TO postgres WITH GRANT OPTION;
GRANT SELECT, USAGE, UPDATE ON SEQUENCE carga_org_lot.tbltokenenviocarga_idtokenenviocarga_seq TO postgres;
