import logging
import logging.handlers
import sys
import os
import configparser
import config
from datetime import datetime, timezone, timedelta

# Configuração padrão
LOG_TO_FILE = True
LOG_TO_SYSLOG = True
MAX_LINES = 1000  # Máximo de linhas
LOG_FILE = 'app.log'

# Função para ler a configuração do syslog do arquivo configure.cfg
def load_syslog_config():
    config = configparser.ConfigParser()
    config.read('configure.cfg')
    
    syslog_ip = config.get('syslog', 'ip', fallback='127.0.0.1')
    syslog_port = config.getint('syslog', 'port', fallback=514)
    enable_remote = config.getboolean('syslog', 'enable_remote', fallback=True)
    return syslog_ip, syslog_port, enable_remote

# Função para verificar o número de linhas no log e sobrescrever se necessário
def check_log_lines():
    try:
        with open(LOG_FILE, 'r') as f:
            lines = f.readlines()
        
        if len(lines) >= MAX_LINES:
            with open(LOG_FILE, 'w') as f:  # Sobrescreve o arquivo
                f.writelines(lines[-MAX_LINES:])  # Mantém apenas as últimas 1000 linhas
    except FileNotFoundError:
        pass  # Se o arquivo não existir, nada precisa ser feito

# Função para configurar o logger
def setup_logger():
    logger = logging.getLogger('app_logger')
    logger.setLevel(logging.DEBUG)

    # Prefixo do hardware - garantindo que seja uma string
    hardware_prefix = str(config.hardware)

    # Definir o fuso horário GMT-3
    gmt_minus_3 = timezone(timedelta(hours=-3))

    def custom_time(*args, **kwargs):
        return datetime.now(gmt_minus_3).strftime('%Y-%m-%d %H:%M:%S')

    # Formato do log
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - [' + hardware_prefix + '] - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')

    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler para arquivo de log (com controle de linhas)
    if LOG_TO_FILE:
        class LineLimitedFileHandler(logging.FileHandler):
            def emit(self, record):
                check_log_lines()  # Checa e sobrescreve se necessário
                super().emit(record)

        file_handler = LineLimitedFileHandler(LOG_FILE, mode='a')  # Mantém o modo de escrita contínua
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Handler para syslog
    if LOG_TO_SYSLOG:
        syslog_ip, syslog_port, enable_remote = load_syslog_config()
        if enable_remote:
            syslog_handler = logging.handlers.SysLogHandler(address=(syslog_ip, syslog_port))
            syslog_handler.setLevel(logging.DEBUG)
            syslog_handler.setFormatter(formatter)
            logger.addHandler(syslog_handler)

    return logger

# Criar o logger global
log = setup_logger()

# Função para gerar logs
def log_message(message, level="info"):
    """Loga uma mensagem com o nível desejado (info, error, etc.)."""
    log_func = getattr(log, level, log.info)
    log_func(message)
