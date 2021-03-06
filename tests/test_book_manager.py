from contextlib import contextmanager
from typing import Callable, Generator, List

import grpc
import pytest

from book_grpc_service.handler.manager import ManagerService
from book_grpc_service.helper.conn_proxy import SteadyDBConnection, g_db_pool
from grpc_example_common.interceptor.server_interceptor.customer_top import CustomerTopInterceptor
from grpc_example_common.protos.book import manager_pb2, manager_pb2_grpc
from grpc_example_common.helper.grpc_wrapper import auto_load_wrapper_by_stub, grpc_client_func_wrapper
from grpc_example_common.interceptor.client_interceptor.customer_top import (
    CustomerTopInterceptor as ClientCustomerTopInterceptor,
)


@pytest.fixture(scope="module")
def grpc_add_to_server() -> Callable:
    return manager_pb2_grpc.add_BookManagerServicer_to_server


@pytest.fixture(scope="module")
def grpc_servicer() -> ManagerService:
    return ManagerService()


@pytest.fixture(scope="module")
def grpc_interceptors() -> List[grpc.ServerInterceptor]:
    return [CustomerTopInterceptor()]


@pytest.fixture(scope="module")
def grpc_stub(grpc_channel: grpc.Channel) -> manager_pb2_grpc.BookManagerStub:
    channel: grpc.Channel = grpc.intercept_channel(
        grpc_channel, ClientCustomerTopInterceptor()
    )
    stub: manager_pb2_grpc.BookManagerStub = manager_pb2_grpc.BookManagerStub(channel)
    auto_load_wrapper_by_stub(stub, grpc_client_func_wrapper)
    return stub


@contextmanager
def mock_book(
    isbn="test_isbn",
    book_author="so1n",
    book_name="gRPC Book",
    book_desc="How to use gRPC",
    book_url="http://so1n.me",
) -> Generator[str, None, None]:
    conn: SteadyDBConnection = g_db_pool.connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO book_info (isbn, book_name, book_author, book_desc, book_url) VALUES (%s, %s, %s, %s, %s)",
                (isbn, book_name, book_author, book_desc, book_url),
            )
            cursor.execute(
                "INSERT INTO book_info (isbn, book_name, book_author, book_desc, book_url) VALUES (%s, %s, %s, %s, %s)",
                (isbn + "aaa", book_name, book_author, book_desc, book_url),
            )
        conn.commit()
        yield isbn
    finally:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM book_info WHERE isbn=%s", (isbn,))
            cursor.execute("DELETE FROM book_info WHERE isbn=%s", (isbn + "aaa",))
        conn.commit()


class TestManager:
    def test_create_book(self, grpc_stub: manager_pb2_grpc.BookManagerStub) -> None:
        try:
            request: manager_pb2.CreateBookRequest = manager_pb2.CreateBookRequest(
                isbn="test_isbn",
                book_author="so1n",
                book_name="gRPC Book",
                book_desc="How to use gRPC",
                book_url="http://so1n.me",
            )
            grpc_stub.create_book(request)
        finally:
            conn: SteadyDBConnection = g_db_pool.connection()
            conn.begin()
            with conn.cursor() as cursor:
                ret: int = cursor.execute(
                    "DELETE FROM book_info WHERE isbn=%s", ("test_isbn",)
                )
            conn.commit()
            assert ret == 1

    def test_delete_book(self, grpc_stub: manager_pb2_grpc.BookManagerStub) -> None:
        with mock_book() as isbn:
            request: manager_pb2.DeleteBookRequest = manager_pb2.DeleteBookRequest(
                isbn=isbn
            )
            grpc_stub.delete_book(request)
            conn: SteadyDBConnection = g_db_pool.connection()
            conn.begin()
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*) as cnt FROM book_info WHERE isbn=%s AND deleted=1",
                    (isbn,),
                )
                assert (cursor.fetchone() or {}).get("cnt", 0) == 1

    def test_get_book(self, grpc_stub: manager_pb2_grpc.BookManagerStub) -> None:
        with mock_book() as isbn:
            request: manager_pb2.GetBookRequest = manager_pb2.GetBookRequest(isbn=isbn)
            response: manager_pb2.GetBookResult = grpc_stub.get_book(request)
            assert response.isbn == isbn

    def test_get_book_list(self, grpc_stub: manager_pb2_grpc.BookManagerStub) -> None:
        with mock_book():
            request: manager_pb2.GetBookListRequest = manager_pb2.GetBookListRequest()
            response: manager_pb2.GetBookListResult = grpc_stub.get_book_list(request)
            assert len(response.result) == 2
