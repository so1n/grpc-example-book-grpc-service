from typing import Callable, List

import grpc
import pytest

from book_grpc_service.handler.social import SocialService
from book_grpc_service.helper.conn_proxy import SteadyDBConnection, g_db_pool
from grpc_example_common.helper.grpc_wrapper import auto_load_wrapper_by_stub, grpc_client_func_wrapper
from grpc_example_common.interceptor.server_interceptor.customer_top import CustomerTopInterceptor
from grpc_example_common.protos.book import social_pb2, social_pb2_grpc
from grpc_example_common.interceptor.client_interceptor.customer_top import (
    CustomerTopInterceptor as ClientCustomerTopInterceptor,
)


@pytest.fixture(scope="module")
def grpc_add_to_server() -> Callable:
    return social_pb2_grpc.add_BookSocialServicer_to_server


@pytest.fixture(scope="module")
def grpc_servicer() -> SocialService:
    return SocialService()


@pytest.fixture(scope="module")
def grpc_interceptors() -> List[grpc.ServerInterceptor]:
    return [CustomerTopInterceptor()]


@pytest.fixture(scope="module")
def grpc_stub(grpc_channel: grpc.Channel) -> social_pb2_grpc.BookSocialStub:
    channel: grpc.Channel = grpc.intercept_channel(
        grpc_channel, ClientCustomerTopInterceptor()
    )
    stub: social_pb2_grpc.BookSocialStub = social_pb2_grpc.BookSocialStub(channel)
    auto_load_wrapper_by_stub(stub, grpc_client_func_wrapper)
    return stub


class TestSocial:
    def test_like_book(self, grpc_stub: social_pb2_grpc.BookSocialStub) -> None:
        isbn: str = "test_isbn"
        uid: str = "66666666"
        try:
            like_request: social_pb2.LikeBookRequest = social_pb2.LikeBookRequest(
                isbn=isbn, like=True, uid=uid
            )
            grpc_stub.like_book(like_request)
            get_book_like_request: social_pb2.GetBookLikesRequest = (
                social_pb2.GetBookLikesRequest(isbn=[isbn])
            )
            get_book_like_result: social_pb2.GetBookLikesListResult = (
                grpc_stub.get_book_like(get_book_like_request)
            )
            assert get_book_like_result.result
            assert get_book_like_result.result[0].book_like == 1

            grpc_stub.like_book(social_pb2.LikeBookRequest(isbn=isbn, like=False, uid=uid))

            get_book_like_result = grpc_stub.get_book_like(get_book_like_request)
            assert get_book_like_result.result
            assert get_book_like_result.result[0].book_like == 0
        finally:
            conn: SteadyDBConnection = g_db_pool.connection()
            with conn.cursor() as cursor:
                ret: int = cursor.execute(
                    "DELETE FROM book_like WHERE isbn=%s", (isbn,)
                )
            conn.commit()
            assert ret == 1

    def test_comment_bool(self, grpc_stub: social_pb2_grpc.BookSocialStub) -> None:
        isbn: str = "test_isbn"
        uid: str = "66666666"
        try:
            comment_book_request: social_pb2.CommentBookRequest = (
                social_pb2.CommentBookRequest(
                    isbn=isbn, content="test content", uid=uid
                )
            )
            grpc_stub.comment_book(request=comment_book_request)
            get_book_comment_request: social_pb2.GetBookCommentRequest = (
                social_pb2.GetBookCommentRequest(isbn=[isbn])
            )
            result: social_pb2.GetBookCommentListResult = grpc_stub.get_book_comment(
                request=get_book_comment_request
            )
            assert result.result
            assert result.result[0].isbn == isbn
        finally:
            conn: SteadyDBConnection = g_db_pool.connection()
            with conn.cursor() as cursor:
                ret: int = cursor.execute(
                    "DELETE FROM book_comment WHERE isbn=%s", (isbn,)
                )
            conn.commit()
            # assert ret == 1
