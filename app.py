import logging
import os
from concurrent import futures
from typing import List, Optional

import grpc

from book_grpc_service.handler.manager import ManagerService, manager_service
from book_grpc_service.handler.social import SocialService, social_service
from grpc_example_common.interceptor.client_interceptor.base import BaseInterceptor
from grpc_example_common.interceptor.client_interceptor.customer_top import CustomerTopInterceptor

logging.basicConfig(
    format="[%(asctime)s %(levelname)s] %(message)s",
    datefmt="%y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)
logger: logging.Logger = logging.getLogger()


def main(
    host: str = "0.0.0.0", port: str = "9000", ssl_port: Optional[str] = None
) -> None:
    interceptor_list: List[BaseInterceptor] = [CustomerTopInterceptor()]
    server: grpc.server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=interceptor_list,
    )
    manager_service.add_BookManagerServicer_to_server(ManagerService(), server)
    social_service.add_BookSocialServicer_to_server(SocialService(), server)

    if ssl_port:
        port = ssl_port
        # read in key and certificate
        with open(os.path.join(os.path.split(__file__)[0], "server.key")) as f:
            private_key = f.read().encode()
        with open(os.path.join(os.path.split(__file__)[0], "server.crt")) as f:
            certificate_chain = f.read().encode()
        # create server credentials
        server_creds = grpc.ssl_server_credentials(
            (
                (
                    private_key,
                    certificate_chain,
                ),
            )
        )
        server.add_secure_port(f"{host}:{port}", server_creds)
    else:
        server.add_insecure_port(f"{host}:{port}")
    server.start()
    try:
        for generic_handler in server._state.generic_handlers:
            logger.info(
                f"add service name:{generic_handler.service_name()} cnt:{len(generic_handler._method_handlers)}"
            )
        logger.info(f"server run in {host}:{port}")
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    main()
