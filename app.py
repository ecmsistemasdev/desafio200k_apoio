import streamlit as st
import mysql.connector
import re
from datetime import date
import smtplib
import email.message

conexao = mysql.connector.connect(
    host='200k.mysql.uhserver.com',
    user='ecm200',
    password='@Musica17',
    database='200k'
)

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


v_nome = ""
v_ncelular = ""
v_quemapoia = ""
v_email = ""

# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

def calculateAge(birthDate): 
    #dia = int(nascimento[0:2])
    #mes = int(nascimento[3:5])
    #ano = int(nascimento[6:10])

    #birthDate = date(ano, mes, dia)

    today = date.today() 
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day)) 
  
    return age 


def enviar_email(snome,sfone,squemapoio,semail): 
    try: 
        corpo_email = f"""
        <p>Inscrição  de apoio realizada para o <b>3º Desafio 200k - Porto Velho/Humaitá</b> </p>
        <p>Nome: <b>{snome}</b> </p>
        <p>Telefone: <b>{sfone}</b> </p>
        <p>Quem apoia: <b>{squemapoio}</b> </p>
        """
        
        msg = email.message.Message()
        msg['Subject'] = "Inscrição de Apoio do 3º Desafio 200k - "+ snome
        msg['From'] = 'ecmsistemasdeveloper@gmail.com'
        msg['To'] = "kelioesteves@hotmail.com;"
        msg['Co'] = semail
        password = 'mwxncuvjvmvwvnhp' 
        msg.add_header('Content-Type', 'text/html')
        #msg.attach()
        msg.set_payload(corpo_email )

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        # Login Credentials for sending the mail
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To'],msg['Co']], msg.as_string().encode('utf-8'))
        s.quit()
        st.write("")
    except Exception as e:
        st.write("")
    #finally:            


def concluido():
    global tela_ativa
    #placeholder.empty()
    #placeholder2 = st.empty()

    #with placeholder2.form("Regulamento"):
    st.success("INSCRIÇÃO REALIZADA COM SUCESSO")
    #st.write(incricao().modalidade)
    #st.write(incricao().idmodalidade)
    #st.write(incricao().kmsolo)
    #st.write("id_atleta ", inscricao().idatleta)



st.set_page_config(page_title="3º Desafio 200k")
tela_ativa = 0

from PIL import Image
img = Image.open('02.png')
st.image(img)

st.markdown("### 3º Desafio 200k - Porto Velho/Humaitá")

form_inscricao = st.empty()

def inscricao():
    global tela_ativa
    global concluido
    global v_nome, v_modalidade, v_ncelular, v_email

    with ((form_inscricao.form("Inscricao"))):
        st.markdown("### Formulário de Inscrição do Apoio")

        input_email = st.text_input(label="E-mail:", key="01")
        input_nome = st.text_input(label="Primeiro Nome:", placeholder="Insira apenas seu primeiro nome", key="02")
        input_sobrenome = st.text_input(label="Sobrenome:", placeholder="Insira seu sobrenome",key="03")
        input_dn = st.date_input(label="Data de Nascimento:",format="DD/MM/YYYY", 
                                 max_value=date(year=2006, month=7, day=5),min_value=date(year=1924, month=7, day=5), value=None, key="05")
        input_telefone = st.text_input(label="Nº Celular 99 99999-9999:", max_chars=15, key="06")
        st.caption("Endereço:")
        e1, e2 = st.columns([4,1])
        with e1:
            input_rua = st.text_input(label="Rua:", key="07")
        with e2:
            input_numero = st.text_input(label="Número:", key="15")
        input_comp = st.text_input(label="Complemento:", key="28")
        input_bairro = st.text_input(label="Bairro:", key="08")
        g1, g2 = st.columns([2, 1])
        with g1:
            input_cidade = st.text_input(label="Cidade:", value="Porto Velho", key="09")
        with g2:
            input_estado = st.selectbox("Estado:",("Acre (AC)",
                                                   "Alagoas (AL)",
                                                   "Amapá (AP)",
                                                   "Amazonas (AM)",
                                                   "Bahia (BA)",
                                                   "Ceará (CE)",
                                                   "Distrito Federal (DF)",
                                                   "Espírito Santo (ES)",
                                                   "Goiás (GO)",
                                                   "Maranhão (MA)",
                                                   "Mato Grosso (MT)",
                                                   "Mato Grosso do Sul (MS)",
                                                   "Minas Gerais (MG)",
                                                   "Pará (PA)",
                                                   "Paraíba (PB)",
                                                   "Paraná (PR)",
                                                   "Pernambuco (PE)",
                                                   "Piauí (PI)",
                                                   "Rio de Janeiro (RJ)",
                                                   "Rio Grande do Norte (RN)",
                                                   "Rio Grande do Sul (RS)",
                                                   "Rondônia (RO)",
                                                   "Roraima (RR)",
                                                   "Santa Catarina (SC)",
                                                   "São Paulo (SP)",
                                                   "Sergipe (SE)",
                                                   "Tocantins (TO)"),index=21)

        f1,f2 = st.columns([1,1])
        with f1:
            input_genero = st.radio("Gênero:", ["Masculino", "Feminino"])
        with f2:
            input_camiseta = st.radio("Camiseta:", ["PP", "P", "M", "G"])

        st.divider()

        input_quemapoia = st.text_input(label="Qual atleta ou equipe você vai apoiar?",key="22")
        
        st.divider()

        st.write("Termo de Responsabilidade")

        def termoResp():
            with open('Termo.txt', 'r', encoding='UTF-8') as f:
                lines = f.readlines()
                for line in lines:
                    st.caption(line)

        termoResp()

        check_resp = False
        flresp = st.checkbox('LI E ACEITO O TERMO DE RESPONSABILIDADE',key="disabled")

        if flresp:
            check_resp = True
        
        st.divider()

        cursor1 = conexao.cursor()
        comando = f'SELECT ID_APOIO FROM 200k.APOIO WHERE EMAIL = "{input_email}"'
        cursor1.execute(comando)
        resultado_email = cursor1.fetchone()
        #s_email = resultado_email[0]

        cursor2 = conexao.cursor()
        id_ = f'SELECT IFNULL(MAX(ID_APOIO)+1,1) FROM APOIO'
        cursor2.execute(id_)
        newid = cursor2.fetchone()
        idapoio = newid[0]

        confirma_button = st.form_submit_button("CONFIRMAR INSCRIÇÃO",type="primary") #, disabled=not st.session_state.disabled)
                                

        if confirma_button:
            if input_email == '':
                st.warning("Informe o E-mail!", icon="⚠️")
                st.stop()

            if not(re.search(regex,input_email)):  
                st.warning("E-mail incorreto", icon="⚠️")   
                st.stop()

            if input_nome == '':
                st.warning("Informe o primeiro Nome!", icon="⚠️")
                st.stop()

            if input_sobrenome == '':
                st.warning("Informe o primeiro Nome!", icon="⚠️")
                st.stop()

            if input_dn == '':
                st.warning("Informe sua Data de Nascimento!", icon="⚠️")
                st.stop()

            if input_telefone == '':
                st.warning("Informe o número do Celular!", icon="⚠️")
                st.stop()

            if input_quemapoia == '':
                st.warning("Informe o atleta ou equipe a qual está apoiando!", icon="⚠️")
                st.stop()

            ncelular = input_telefone
            crtr1 = "!@#$()*'%:;?<>_\|/ .-,"
            for i in range(0,len(crtr1)):
                ncelular = ncelular.replace(crtr1[i],"")

            if len(ncelular) is not 11:
                st.warning("Nº do celular inválido")
                st.stop()

            if input_rua == '':
                st.warning("Informe a Rua!", icon="⚠️")
                st.stop()

            if input_bairro == '':
                st.warning("Informe o Bairro!", icon="⚠️")
                st.stop()

            if input_cidade == '':
                st.warning("Informe a Cidade e Estado (UF)!", icon="⚠️")
                st.stop()

            if resultado_email is not None:
                st.warning("E-mail Já cadastrado!", icon="⚠️")
                st.stop()

            if not check_resp:
                st.warning("Necessário aceitar o Termo de Responsabilidade!", icon="⚠️")
                st.stop()

            if input_genero == 'Masculino':
                sexo = "M"
            else:
                sexo = "F"

            data = date.today()
            dataf = data.strftime('%d/%m/%Y')
            datanasc = input_dn.strftime('%d/%m/%Y')
            idade = calculateAge(input_dn)
            
            v_nome = input_nome + ' ' + input_sobrenome
            v_ncelular = ncelular
            v_email = input_email
            v_quemapoia = input_quemapoia

            try:

                qry_insert = f"""INSERT INTO 200k.APOIO (
                                 ID_APOIO, EMAIL, NOME, ENDERECO, NR_ENDERECO, COMP_ENDERECO, CIDADE, ESTADO_UF, DT_NASCIMENTO, 
                                 NR_CELULAR, SEXO, CAMISETA, QUEM_APOIA, ATIVO, DT_INSCRICAO, FL_TERMO)
                                 VALUES (
                                        {idapoio},"{input_email}","{input_nome + ' ' + input_sobrenome}","{input_rua}","{input_numero}","{input_comp}","{input_cidade}",
                                        "{input_estado}","{datanasc}","{ncelular}","{sexo}","{input_camiseta}","{v_quemapoia}",'Sim',"{dataf}",'S') """

                cursor = conexao.cursor()
                cursor.execute(qry_insert)
                conexao.commit()
                cursor.close()

            except mysql.connector.Error as error:
                st.warning("Erro no Banco de Daods, tente novamente, se persistir contate o Administrador do Sistema! {}".format(error), icon="⚠️")
                st.stop()

            finally:
                if conexao.is_connected():
                    conexao.close()            
        
            tela_ativa = 2

            form_inscricao.empty()

inscricao()

if tela_ativa == 2:

    st.success("INSCRIÇÃO REALIZADA COM SUCESSO", icon="😀")
    #st.warning("ATENÇÃO", icon="⚠️")
    st.warning("Em caso de dúvidas e pra mais esclarecimento, entrar em contato atraves do número (69) 99925-9005, ou pelo link a baixo:")
    st.warning("https://wa.me/5569999259005", icon="📱")

    enviar_email(v_nome,v_ncelular,v_quemapoia,v_email)

from PIL import Image
img = Image.open('003.png')
st.image(img)
