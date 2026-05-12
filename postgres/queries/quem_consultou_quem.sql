WITH Paciente AS (
	SELECT
		PAC.pacienteid AS PACIENTE_ID, 
		PES.NOME AS NOME_PACIENTE,
		PES.cpf AS CPF_PACIENTE
	FROM ccd410.paciente PAC
	INNER JOIN ccd410.pessoa PES ON PAC.pessoaid = PES.pessoaid
),
Medico AS (
	SELECT
		FUNC.funcionarioid AS MEDICO_ID,
		PES.NOME AS NOME_MEDICO,
		PES.cpf AS CPF_MEDICO
	FROM ccd410.funcionario FUNC
	INNER JOIN ccd410.pessoa PES ON FUNC.pessoaid = PES.pessoaid
)

SELECT
	C.dtconsulta AS DT_CONSULTA,
	C.retorno AS RETORNO,
	C.descricao AS DESCRICAO,
	C.encaminhamento AS ENCAMINHAMENTO,
	M.NOME_MEDICO AS MEDICO,
	P.NOME_PACIENTE AS PACIENTE
FROM ccd410.consulta C
INNER JOIN Medico M ON C.funcionarioid = MEDICO_ID
INNER JOIN Paciente P ON C.pacienteid = PACIENTE_ID