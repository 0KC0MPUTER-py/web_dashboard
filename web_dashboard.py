import shutil
import streamlit as st
import subprocess
import platform

# Configuração da página
st.set_page_config(
    page_title="Painel de Ferramentas de Rede",
    layout="wide"
)

st.title("🌐 Dashboard de Suporte de TI")
st.markdown("Execute ferramentas de diagnóstico sem abrir o terminal.")

sistema = platform.system()

# Menu lateral
ferramenta = st.sidebar.selectbox(
    "Escolha a ferramenta:",
    [
        "Informações de Rede",
        "Teste de Ping",
        "Traçado de Rota (Traceroute)",
        "Nmap Scan"
    ]
)

# -------------------------------
# Informações de Rede
# -------------------------------
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
            st.error("Comando não encontrado.")

        except subprocess.CalledProcessError as e:
            st.error(
                f"Erro ao executar o comando "
                f"(status {e.returncode}):\n"
                f"{e.stderr or e.stdout}"
            )

# -------------------------------
# Ping
# -------------------------------
elif ferramenta == "Teste de Ping":
    st.header("⚡ Teste de Conectividade")

    host = st.text_input(
        "Digite o IP ou URL:",
        "8.8.8.8"
    )

    if st.button("Rodar Ping"):
        if not host.strip():
            st.warning("Digite um host válido.")
        else:
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
                st.error(
                    f"Ping falhou "
                    f"(status {e.returncode}):\n"
                    f"{e.stderr or e.stdout}"
                )

# -------------------------------
# Traceroute
# -------------------------------
elif ferramenta == "Traçado de Rota (Traceroute)":
    st.header("🛰️ Traçado de Rota")

    host = st.text_input(
        "Digite o IP ou URL:",
        "google.com"
    )

    if st.button("Executar Traceroute"):
        if not host.strip():
            st.warning("Digite um host válido.")
        else:
            comando = (
                ["tracert", host]
                if sistema == "Windows"
                else ["traceroute", host]
            )

            try:
                resultado = subprocess.run(
                    comando,
                    capture_output=True,
                    text=True,
                    check=True
                )

                st.subheader("Resultado:")
                st.code(resultado.stdout)

            except FileNotFoundError:
                st.error(
                    "Comando traceroute/tracert não encontrado."
                )

            except subprocess.CalledProcessError as e:
                st.error(
                    f"Traceroute falhou "
                    f"(status {e.returncode}):\n"
                    f"{e.stderr or e.stdout}"
                )

# -------------------------------
# Nmap
# -------------------------------
elif ferramenta == "Nmap Scan":
    st.header("🛡️ Scanner Nmap")

    host = st.text_input(
        "Digite o IP ou URL:",
        "scanme.nmap.org"
    )
    ports = st.text_input(
        "Portas (ex: 1-1024):",
        "1-1024"
    )
    scan_type = st.selectbox(
        "Tipo de varredura:",
        ["Normal", "Ping", "Serviços/Versão"]
    )

    if st.button("Executar Nmap"):
        if not host.strip():
            st.warning("Digite um host válido.")
        else:
            if shutil.which("nmap") is None:
                st.error(
                    "Nmap não encontrado. Instale o Nmap e adicione-o ao PATH."
                )
            else:
                comando = ["nmap"]

                if scan_type == "Ping":
                    comando.append("-sn")
                elif scan_type == "Serviços/Versão":
                    comando.append("-sV")

                if scan_type != "Ping":
                    comando += ["-p", ports]

                comando.append(host)

                try:
                    resultado = subprocess.run(
                        comando,
                        capture_output=True,
                        text=True,
                        check=True
                    )

                    st.subheader("Resultado:")
                    st.code(resultado.stdout)

                except FileNotFoundError:
                    st.error("Comando nmap não encontrado.")

                except subprocess.CalledProcessError as e:
                    st.error(
                        f"Nmap falhou "
                        f"(status {e.returncode}):\n"
                        f"{e.stderr or e.stdout}"
                    )
