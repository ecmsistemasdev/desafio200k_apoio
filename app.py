import streamlit as st
import mysql.connector
import re
from datetime import datetime
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
#v_modalidade = ""
#v_email = ""

# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

def enviar_email(snome,sfone,semail): 
    try: 
        corpo_email = f"""
        <p>Feijoada do Casório</b> </p>
        <p>Nome: <b>{snome}</b> </p>
        <p>Telefone: <b>{sfone}</b> </p>
        """
        
        msg = email.message.Message()
        msg['Subject'] = "Feijoada do Casório - "+ snome
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
    st.success("PEDIDO REALIZADO COM SUCESSO")




st.set_page_config(page_title="Feijoada do Casório")
tela_ativa = 0

from PIL import Image
img = Image.open('02.png')
st.image(img)

st.markdown("### Feijoada do Casório")


form_inscricao = st.empty()

def inscricao():
    global tela_ativa
    global concluido
    global v_nome, v_ncelular

    with ((form_inscricao.form("Inscricao"))):
        #input_email = st.text_input(label="E-mail:", key="01")
        input_nome = st.text_input(label="Nome:", placeholder="Informe seu nome", key="01")
        input_telefone = st.text_input(label="Nº Celular 99 99999-9999:", max_chars=15, key="02")
        input_re = st.radio("Entrega/Retirada:", ["Entrega", "Retirada"], key="03")

        st.caption("Endereço:")
        e1, e2 = st.columns([4,1])
        with e1:
            input_rua = st.text_input(label="Rua:", key="04")
        with e2:
            input_numero = st.text_input(label="Número:", key="05")
        input_comp = st.text_input(label="Complemento:", key="06")
        input_bairro = st.text_input(label="Bairro:", key="07")
        input_pontoref = st.text_input(label="Ponto de referência:", key="08")
        input_obs = st.text_input(label="Observações:", key="09")

        #input_cidade = st.text_input(label="Cidade/UF:", value="Porto Velho/RO", key="08")

        st.divider()

        cursorID = conexao.cursor()
        id_ = f'SELECT IFNULL(MAX(ID_PEDIDO)+1,1) FROM FEIJOADA'
        cursorID.execute(id_)
        newid = cursorID.fetchone()
        idpedido = newid[0]

        confirma_button = st.form_submit_button("CONFIRMAR PEDIDO",type="primary") #, disabled=not st.session_state.disabled)
                                

        if confirma_button:
            if input_nome == '':
                st.warning("Informe seu Nome!", icon="⚠️")
                st.stop()

            if input_telefone == '':
                st.warning("Informe o número do Celular!", icon="⚠️")
                st.stop()

            ncelular = input_telefone
            crtr1 = "!@#$()*'%:;?<>_\|/ .-,"
            for i in range(0,len(crtr1)):
                ncelular = ncelular.replace(crtr1[i],"")

            if len(ncelular) is not 11:
                st.warning("Nº do celular inválido")
                st.stop()

            if input_re == 'Entrega':
                if input_rua == '':
                    st.warning("Informe a Rua!", icon="⚠️")
                    st.stop()

                if input_numero == '':
                    st.warning("Informe o Número de endereço!", icon="⚠️")
                    st.stop()

                if input_bairro == '':
                    st.warning("Informe o Bairro!", icon="⚠️")
                    st.stop()

            if input_re == 'Entrega':
                s_re = "E"
            else:
                s_re = "R"

            data_e_hora = datetime.now()
            dtpedido = data_e_hora.strftime('%d/%m/%Y %H:%M')
            
            v_ncelular = ncelular

            try:

                qry_insert = f"""INSERT INTO 200k.FEIJOADA (
                                 ID_PEDIDO, NOME, ENDERECO, NR_ENDERECO, COMP_ENDERECO, PONTO_REF, BAIRRO, NR_CELULAR, 
                                 FL_RE, OBS, DATAHORA_PEDIDO)
                                 VALUES (
                                        {idpedido},"{input_nome}","{input_rua}","{input_numero}","{input_comp}","{input_pontoref}",
                                        "{input_bairro}","{ncelular}","{s_re}","{input_obs}","{dtpedido}") """

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

    st.success("PEDIDO REALIZADO COM SUCESSO", icon="😀")
    #st.warning("ATENÇÃO", icon="⚠️")
    st.warning("Em caso de dúvidas e pra mais esclarecimento, entrar em contato atraves do número (69) 99291-0753, ou pelo link a baixo:")
    st.warning("https://wa.me/5569992910753", icon="📱")

    pessoa = v_nome
    numero = '55' + v_ncelular
    texto = f"Nome: {pessoa}! {' Teste'}"
    st.warning("https://web.whatsapp.com/send?phone={numero}&text={texto}", icon="📱")


    #enviar_email(v_nome,v_ncelular,v_email)

from PIL import Image
img = Image.open('003.png')
st.image(img)

