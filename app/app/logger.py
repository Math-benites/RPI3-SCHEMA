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
MAX_LINES = 1000  # Defina o número máximo de linhas
LOG_FILE = 'app.log'

# Função para ler a configuração do syslog do arquivo configure.cfg
def load_syslog_config():
    config = configparser.ConfigParser()
    config.read('configure.cfg')  # Mudamos para 'configure.cfg'
    
    syslog_ip = config.get('syslog', 'ip', fallback='127.0.0.1')  # Valor padrão 127.0.0.1
    syslog_port = config.getint('syslog', 'port', fallback=514)  # Valor padrão 514
    enable_remote = config.getboolean('syslog', 'enable_remote', fallback=True)  # Valor padrão True
    return syslog_ip, syslog_port, enable_remote

# Função para calcular o tamanho máximo do arquivo com base nas linhas
def get_max_file_size():
    try:
        with open(LOG_FILE, 'r') as f:
            lines = f.readlines()
            return sum(len(line) for line in lines) * MAX_LINES // len(lines) if lines else 1024 * 10  # 10KB por padrão
    except FileNotFoundError:
        return 1024 * 10  # Caso o arquivo não exista, usa 10KB como valor inicial

# Função para configurar o logger
def setup_logger():
    logger = logging.getLogger('app_logger')
    logger.setLevel(logging.DEBUG)

    # Prefixo do hardware - garantindo que seja uma string
    hardware_prefix = str(config.hardware)  # Convertendo para string

    # Definir o fuso horário GMT-3
    gmt_minus_3 = timezone(timedelta(hours=-3))

    # Função para obter o tempo com o fuso horário ajustado
    def custom_time(*args, **kwargs):
        return datetime.now(gmt_minus_3).strftime('%Y-%m-%d %H:%M:%S')

    # Adicionar handler para exibir logs no console com o prefixo de hardware
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - [' + hardware_prefix + '] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Adicionar handler para salvar logs em arquivo com limitação de tamanho
    if LOG_TO_FILE:
        max_size = get_max_file_size()
        rotating_handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=max_size, backupCount=3)
        rotating_handler.setLevel(logging.DEBUG)
        rotating_handler.setFormatter(console_formatter)
        logger.addHandler(rotating_handler)

    # Adicionar handler para syslog (opcional)
    if LOG_TO_SYSLOG:
        syslog_ip, syslog_port, enable_remote = load_syslog_config()  # Carregar IP, porta e se remoto está habilitado
        if enable_remote:  # Só configura o syslog remoto se a opção estiver habilitada
            syslog_handler = logging.handlers.SysLogHandler(address=(syslog_ip, syslog_port))
            syslog_handler.setLevel(logging.DEBUG)
            syslog_handler.setFormatter(console_formatter)
            logger.addHandler(syslog_handler)

    # Substituindo o método `asctime` para o custom_time
    logging.Formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
    logging.Formatter.default_msec_format = '%s.%03d'

    return logger

# Cria o logger global para uso
log = setup_logger()

# Função para gerar logs
def log_message(message, level="info"):
    """Loga uma mensagem com o nível desejado (info, error, etc.)."""
    log_func = getattr(log, level, log.info)
    log_func(message)
