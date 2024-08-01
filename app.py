import streamlit as st
import mysql.connector
import re
from datetime import datetime
import smtplib
import email.message
import os
#import locale

conexao = mysql.connector.connect(
    host='200k.mysql.uhserver.com',
    user='ecm200',
    password='@Musica17',
    database='200k'
)

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

v_nome = ""
v_ncelular = ""
v_bool_re = ""
v_endereco = ""
v_numero = ""
v_bairro = ""
v_comp = ""
v_pontoref = ""
v_qtd = 1
v_valor = 45
v_total = 45
v_taxa = 0
v_obs = ""
v_er = ""
vltotal = 0
qtde = 0
RetEnt = ""

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


#def moeda(xvalor):
#    #Xvalor = 1768 
#    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
#    xvalor = locale.currency(xvalor, grouping=True, symbol=None)
#    return 'Valor R$: %s' % xvalor
    # resultado: Valor: 1.768,00


def concluido():
    global tela_ativa

    st.success("PEDIDO REALIZADO COM SUCESSO")


st.set_page_config(page_title="Feijoada do Casório")
tela_ativa = 0

#if tela_ativa==0:
placeholder = st.empty()
with placeholder.container():
    
    from PIL import Image
    img = Image.open('02.png')
    st.image(img)
    st.markdown("### Feijoada do Casório")
    st.caption("Sábado, 10 de agosto de 2024")
    st.caption("")
    st.markdown("##### Obrigado por nos ajudar a realizar esse sonho!")
    st.caption("")
    st.markdown("###### Taxa de entrega R$5,00")
    #st.markdown("###### Caso deseje retirar no local, marque a opção abaixo 👇")

    # Store the initial value of widgets in session state
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False
        st.session_state.values = True

    input_re1 = st.radio("Escolha a opção:", ["Entrega", "Retirada"], disabled=st.session_state.disabled,
                         horizontal=True)

form_pedido = st.empty()

def fmpedido():

    global tela_ativa
    global concluido
    global vltotal
    global qtde
    global RetEnt

    with ((form_pedido.form("pedido",border=False))):

        input_nome = st.text_input(label="Nome:", placeholder="Informe seu nome", key="91")
        input_telefone = st.text_input(label="Nº Celular 99 99999-9999:", max_chars=15, key="652")
        input_qt = st.number_input("Quantidade", min_value=1, max_value=100, value=1)
        v_qtd = input_qt
        v_valor = v_qtd * 45

        # Every form must have a submit button.
        #st.form_submit_button("",disabled=True)


        if input_re1 == "Entrega":
    
            v_total = v_valor + 5
            #st.text("Entrega")
            v_er = "E"
            v_taxa = 5

            st.caption("Endereço:")
            e1, e2 = st.columns([4, 1])
            with e1:
                input_rua = st.text_input(label="Rua:", key="04", disabled=st.session_state.disabled, )
            with e2:
                input_numero = st.text_input(label="Número:", key="05", disabled=st.session_state.disabled, )
            input_comp = st.text_input(label="Complemento:", key="06", disabled=st.session_state.disabled, )
            input_bairro = st.text_input(label="Bairro:", key="07", disabled=st.session_state.disabled, )
            input_pontoref = st.text_input(label="Ponto de referência:", key="08", disabled=st.session_state.disabled, )

            v_endereco = input_rua
            v_numero = input_numero
            v_bairro = input_bairro
            v_comp = input_comp
            v_pontoref = input_pontoref

        else:
            #st.text("Retirada")
            v_er = "R"
            v_taxa = 0
            v_total = v_valor

            v_endereco = ""
            v_numero = ""
            v_bairro = ""
            v_comp = ""
            v_pontoref = ""

        input_obs = st.text_input(label="Observações:", key="09")
        v_obs = input_obs
        
        if input_re1 == "Retirada":
            st.warning("Local para Retirada: Rua Coimbra, 5023 - Flodoaldo pontes Pinto", icon="📍")
            st.page_link("https://www.google.com/maps/place/R.+Coimbra,+5023+-+Flodoaldo+Pontes+Pinto,+Porto+Velho+-+RO,+76820-556/@-8.74851,-63.8687943,17z/data=!3m1!4b1!4m5!3m4!1s0x92325caa5b627c6f:0x2a526fea2c60ceae!8m2!3d-8.7485153!4d-63.8662194?entry=ttu",
                         label="Clique aqui pra ver a localização")
            
        buttom_confirma =  st.form_submit_button("CONFIRMAR PEDIDO", type="primary")  # not st.session_state.disabled)

    #confirma_button = st.button("CONFIRMAR PEDIDO", type="primary")  # , disabled=not st.session_state.disabled)

        if buttom_confirma:
            #v_nome = input_nome
            #v_ncelular = input_telefone
            #v_qtd = input_qt

            if input_nome == '':
                st.warning("Informe seu Nome!", icon="⚠️")
                st.stop()

            if input_telefone == '':
                st.warning("Informe o número do Celular!", icon="⚠️")
                st.stop()

            ncelular = input_telefone
            crtr1 = "!@#$()*'%:;?<>_\|/ .-,"
            for i in range(0, len(crtr1)):
                ncelular = ncelular.replace(crtr1[i], "")

            if len(ncelular) is not 11:
                st.warning("Nº do celular inválido")
                st.stop()

            if v_er == "R":
                s_re = "R"
            else:
                s_re = "E"
                if v_endereco == '':
                    st.warning("Informe a Rua!", icon="⚠️")
                    st.stop()

                if v_numero == '':
                    st.warning("Informe o Número de endereço!", icon="⚠️")
                    st.stop()

                if v_bairro == '':
                    st.warning("Informe o Bairro!", icon="⚠️")
                    st.stop()

            cursorID = conexao.cursor()
            id_ = f'SELECT IFNULL(MAX(ID_PEDIDO)+1,1) FROM FEIJOADA'
            cursorID.execute(id_)
            newid = cursorID.fetchone()
            idpedido = newid[0]

            data_e_hora = datetime.now()
            dtpedido = data_e_hora.strftime('%d/%m/%Y %H:%M')

            try:

                qry_insert = f"""INSERT INTO 200k.FEIJOADA (
                             ID_PEDIDO, NOME, ENDERECO, NR_ENDERECO, COMP_ENDERECO, PONTO_REF, BAIRRO, NR_CELULAR, 
                             FL_RE, OBS, DATAHORA_PEDIDO, QTDE, VL_PEDIDO, VL_ENTREGA, VL_TOTAL)
                             VALUES (
                                    {idpedido},"{input_nome}","{v_endereco}","{v_numero}","{v_comp}","{v_pontoref}","{v_bairro}",
                                    "{ncelular}","{s_re}","{input_obs}","{dtpedido}",{v_qtd},{v_valor},{v_taxa},{v_total}) """

                cursor = conexao.cursor()
                cursor.execute(qry_insert)
                conexao.commit()
                cursor.close()

                vltotal = v_total
                qtde = v_qtd
                RetEnt = s_re


            except mysql.connector.Error as error:
                st.warning(
                    "Erro no Banco de Daods, tente novamente, se persistir contate o Administrador do Sistema! {}".
                        format(error), icon="⚠️")
                st.stop()

            finally:
                if conexao.is_connected():
                    conexao.close()
   
            tela_ativa = 2

            placeholder.empty()
            form_pedido.empty()

fmpedido()

if tela_ativa == 2:

    s_valor = "Valor R$: "+str(vltotal)+",00";
    s_qtd = " - Quantidade: "+str(qtde)
    
    st.success("PEDIDO REALIZADO COM SUCESSO", icon="😀")
    st.success(s_valor + s_qtd, icon="💲")
    st.success("PIX para pagamento: (69) 99291-0753  \n Nome: Lucas Nascimento Pereira - Banco: NuBank", icon="📱")
    #st.warning("ATENÇÃO", icon="⚠️")
    if RetEnt=="R":
        st.warning("Local para Retirada: Rua Coimbra, 5023 - Flodoaldo pontes Pinto", icon="📍")
        st.page_link("https://www.google.com/maps/place/R.+Coimbra,+5023+-+Flodoaldo+Pontes+Pinto,+Porto+Velho+-+RO,+76820-556/@-8.74851,-63.8687943,17z/data=!3m1!4b1!4m5!3m4!1s0x92325caa5b627c6f:0x2a526fea2c60ceae!8m2!3d-8.7485153!4d-63.8662194?entry=ttu",
                     label="Clique aqui pra ver a localização")

    st.success("Em caso de dúvidas e pra mais esclarecimento, entrar em contato atraves do número (69) 99291-0753, ou pelo link a baixo:")
    st.success("https://wa.me/5569992910753", icon="📱")

    
    pessoa = v_nome
    #numero = '55' + v_ncelular
    #texto = f"Nome: {pessoa}! {' Teste'}"

    #enviar_email(v_nome,v_ncelular,v_email)

from PIL import Image
img = Image.open('003.png')
st.image(img)
