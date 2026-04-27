from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from app.core.config import settings

def validate_ssh_connection(ip_address: str, username: str, password: str, port: int = 22, device_type: str = "cisco_ios") -> tuple[bool, str]:
    device = {"device_type": device_type, "host": ip_address, "username": username, "password": password, "port": port, "timeout": settings.SSH_TIMEOUT}
    try:
        connection = ConnectHandler(**device)
        connection.disconnect()
        return True, "Conexión SSH exitosa"
    except NetmikoAuthenticationException:
        return False, "Error de autenticación SSH"
    except NetmikoTimeoutException:
        return False, "Timeout o switch inaccesible"
    except Exception as e:
        return False, f"Error SSH: {str(e)}"
