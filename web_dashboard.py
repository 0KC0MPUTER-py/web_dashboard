import streamlit as st
import subprocess
import platform

st.set_page_config(page_title="Painel de Ferramentas de Rede", layout="wide")

st.title("🌐 Dashboard de Suporte de TI")
st.markdown("Execute ferramentas de diagnóstico sem abrir o terminal.")

sistema = platform.system()

ferramenta = st.sidebar.selectbox( 
    "Escolha a ferramenta:",
    ["Informações de Rede", "Teste de Ping", "Traçado de Rota (Traceroute)"]
)

if ferramenta == "Informações de Rede":
    st.header("📋 Configurações de Interface")
    if st.button("Obter Dados"):
        comando = ["ipconfig"] if sistema == "Windows" else ["ip", "addr"]
        try:
            resultado = subprocess.run(
                comando,
                capture_output=True,
                text=True,
                check=True
            )
            st.code(resultado.stdout)
        except FileNotFoundError:
            st.error("Comando não encontrado. No Linux, instale iproute2 ou use outra distro.")
        except subprocess.CalledProcessError as e:
            st.error(f"Erro ao executar o comando (status {e.returncode}):\n{e.stderr or e.output}")

elif ferramenta == "Teste de Ping":
    st.header("⚡ Teste de Conectividade")
    host = st.text_input("Digite o IP ou URL (ex: google.com)", "8.8.8.8")

    if st.button("Rodar Ping"):
        param = "-n" if sistema == "Windows" else "-c"
        comando = ["ping", param, "4", host]
        try:
            processo = subprocess.run(
                comando,
                capture_output=True,
                text=True,
                check=True
            )
            st.subheader("Resultado:")
            st.code(processo.stdout)
        except FileNotFoundError:
            st.error("Comando ping não encontrado.")
        except subprocess.CalledProcessError as e:
            st.error(f"Ping falhou (status {e.returncode}):\n{e.stderr or e.stdout}")
