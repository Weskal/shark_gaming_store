import json
import redis
import time
import logging
import sys
from app import create_app
from app.database import db
from app.models.product import Product
from sqlalchemy import select

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = create_app()

cfg = app.config
r = redis.Redis(
    host=cfg["REDIS_HOST"],
    port=cfg["REDIS_PORT"],
    db=cfg["REDIS_DB"],
    decode_responses=True
)
queue = cfg["PRODUCT_QUEUE"]

def process_message(msg):
    op = msg["op"]
    data = msg["data"]

    try:
        if op == "create":
            p = Product(
                name=data["name"], #type: ignore
                brand=data.get("brand"), #type: ignore
                price=data["price"] #type: ignore
            )
            db.session.add(p)
            db.session.commit()
            logger.info(f"CREATE: Produto criado - ID={p.id}, Nome='{p.name}', Marca='{p.brand}', Preço={p.price}")

        elif op == "update":
            product_id = data["id"]
            # Método correto para SQLAlchemy 2.x
            p = db.session.get(Product, product_id)
            
            if not p:
                logger.warning(f"UPDATE: Produto ID={product_id} não encontrado no banco")
                return
            
            # Log dos valores antigos
            logger.info(f"UPDATE: Atualizando produto ID={p.id} - Valores antigos: Nome='{p.name}', Marca='{p.brand}', Preço={p.price}")
            
            if "name" in data:
                p.name = data["name"]
            if "brand" in data:
                p.brand = data["brand"]
            if "price" in data:
                p.price = data["price"]
            
            db.session.commit()
            logger.info(f"UPDATE: Produto ID={p.id} atualizado - Novos valores: Nome='{p.name}', Marca='{p.brand}', Preço={p.price}")

        elif op == "delete":
            product_id = data["id"]
            # Método correto para SQLAlchemy 2.x
            p = db.session.get(Product, product_id)
            
            if not p:
                logger.warning(f"DELETE: Produto ID={product_id} não encontrado no banco")
                return
            
            # Log antes de deletar
            logger.info(f"DELETE: Deletando produto ID={product_id}, Nome='{p.name}', Marca='{p.brand}'")
            
            db.session.delete(p)
            db.session.commit()
            logger.info(f"DELETE: Produto ID={product_id} removido com sucesso do banco de dados")

        else:
            logger.warning(f"Operação desconhecida recebida: '{op}'")

    except KeyError as e:
        logger.error(f"ERRO: Campo obrigatório ausente na mensagem - {str(e)}")
        db.session.rollback()
        
    except Exception as e:
        logger.error(f"ERRO ao processar operação '{op}': {str(e)}", exc_info=True)
        db.session.rollback()
        raise


if __name__ == "__main__":
    logger.info(f"=== Worker iniciado ===")
    logger.info(f"Fila Redis: '{queue}'")
    logger.info(f"Redis Host: {cfg['REDIS_HOST']}:{cfg['REDIS_PORT']}")
    logger.info(f"Aguardando mensagens...")

    with app.app_context():
        while True:
            try:
                item = r.brpop(queue, timeout=5)
                if not item:
                    continue
                
                _, raw = item #type: ignore
                logger.info(f"--- Nova mensagem recebida ---")
                logger.debug(f"Raw payload: {raw}")
                
                msg = json.loads(raw)
                logger.info(f"Operação: '{msg.get('op')}' | Dados: {msg.get('data')}")
                
                process_message(msg)
                logger.info(f"--- Mensagem processada com sucesso ---\n")

            except json.JSONDecodeError as e:
                logger.error(f"ERRO: JSON inválido recebido - {e}")
                logger.error(f"Payload recebido: {raw if 'raw' in locals() else 'N/A'}")
                
            except redis.ConnectionError as e:
                logger.error(f"ERRO: Falha na conexão com Redis - {e}")
                time.sleep(5)
                
            except Exception as e:
                logger.error(f"ERRO no loop principal: {str(e)}", exc_info=True)
                time.sleep(2)