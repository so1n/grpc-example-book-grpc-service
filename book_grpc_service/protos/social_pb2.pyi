"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import google.protobuf.timestamp_pb2
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor = ...

class LikeBookRequest(google.protobuf.message.Message):
    """user upvote&unlike book"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    ISBN_FIELD_NUMBER: builtins.int
    LIKE_FIELD_NUMBER: builtins.int
    UID_FIELD_NUMBER: builtins.int
    isbn: typing.Text = ...
    like: builtins.bool = ...
    uid: typing.Text = ...
    def __init__(
        self,
        *,
        isbn: typing.Text = ...,
        like: builtins.bool = ...,
        uid: typing.Text = ...,
    ) -> None: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "isbn", b"isbn", "like", b"like", "uid", b"uid"
        ],
    ) -> None: ...

global___LikeBookRequest = LikeBookRequest

class GetBookLikesRequest(google.protobuf.message.Message):
    """get book likes"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    ISBN_FIELD_NUMBER: builtins.int
    @property
    def isbn(
        self,
    ) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[
        typing.Text
    ]: ...
    def __init__(
        self,
        *,
        isbn: typing.Optional[typing.Iterable[typing.Text]] = ...,
    ) -> None: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["isbn", b"isbn"]
    ) -> None: ...

global___GetBookLikesRequest = GetBookLikesRequest

class GetBookLikesResult(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    ISBN_FIELD_NUMBER: builtins.int
    BOOK_LIKE_FIELD_NUMBER: builtins.int
    isbn: typing.Text = ...
    book_like: builtins.int = ...
    def __init__(
        self,
        *,
        isbn: typing.Text = ...,
        book_like: builtins.int = ...,
    ) -> None: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "book_like", b"book_like", "isbn", b"isbn"
        ],
    ) -> None: ...

global___GetBookLikesResult = GetBookLikesResult

class GetBookLikesListResult(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    RESULT_FIELD_NUMBER: builtins.int
    @property
    def result(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[
        global___GetBookLikesResult
    ]: ...
    def __init__(
        self,
        *,
        result: typing.Optional[typing.Iterable[global___GetBookLikesResult]] = ...,
    ) -> None: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["result", b"result"]
    ) -> None: ...

global___GetBookLikesListResult = GetBookLikesListResult

class CommentBookRequest(google.protobuf.message.Message):
    """book comment"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    ISBN_FIELD_NUMBER: builtins.int
    CONTENT_FIELD_NUMBER: builtins.int
    UID_FIELD_NUMBER: builtins.int
    isbn: typing.Text = ...
    content: typing.Text = ...
    uid: typing.Text = ...
    def __init__(
        self,
        *,
        isbn: typing.Text = ...,
        content: typing.Text = ...,
        uid: typing.Text = ...,
    ) -> None: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "content", b"content", "isbn", b"isbn", "uid", b"uid"
        ],
    ) -> None: ...

global___CommentBookRequest = CommentBookRequest

class GetBookCommentRequest(google.protobuf.message.Message):
    """get book comment"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    ISBN_FIELD_NUMBER: builtins.int
    NEXT_CREATE_TIME_FIELD_NUMBER: builtins.int
    LIMIT_FIELD_NUMBER: builtins.int
    @property
    def isbn(
        self,
    ) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[
        typing.Text
    ]: ...
    @property
    def next_create_time(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    limit: builtins.int = ...
    def __init__(
        self,
        *,
        isbn: typing.Optional[typing.Iterable[typing.Text]] = ...,
        next_create_time: typing.Optional[
            google.protobuf.timestamp_pb2.Timestamp
        ] = ...,
        limit: builtins.int = ...,
    ) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions.Literal[
            "_limit",
            b"_limit",
            "_next_create_time",
            b"_next_create_time",
            "limit",
            b"limit",
            "next_create_time",
            b"next_create_time",
        ],
    ) -> builtins.bool: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "_limit",
            b"_limit",
            "_next_create_time",
            b"_next_create_time",
            "isbn",
            b"isbn",
            "limit",
            b"limit",
            "next_create_time",
            b"next_create_time",
        ],
    ) -> None: ...
    @typing.overload
    def WhichOneof(
        self, oneof_group: typing_extensions.Literal["_limit", b"_limit"]
    ) -> typing.Optional[typing_extensions.Literal["limit"]]: ...
    @typing.overload
    def WhichOneof(
        self,
        oneof_group: typing_extensions.Literal[
            "_next_create_time", b"_next_create_time"
        ],
    ) -> typing.Optional[typing_extensions.Literal["next_create_time"]]: ...

global___GetBookCommentRequest = GetBookCommentRequest

class GetBookCommentResult(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    ISBN_FIELD_NUMBER: builtins.int
    CONTENT_FIELD_NUMBER: builtins.int
    UID_FIELD_NUMBER: builtins.int
    CREATE_TIME_FIELD_NUMBER: builtins.int
    isbn: typing.Text = ...
    content: typing.Text = ...
    uid: typing.Text = ...
    @property
    def create_time(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    def __init__(
        self,
        *,
        isbn: typing.Text = ...,
        content: typing.Text = ...,
        uid: typing.Text = ...,
        create_time: typing.Optional[google.protobuf.timestamp_pb2.Timestamp] = ...,
    ) -> None: ...
    def HasField(
        self, field_name: typing_extensions.Literal["create_time", b"create_time"]
    ) -> builtins.bool: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "content",
            b"content",
            "create_time",
            b"create_time",
            "isbn",
            b"isbn",
            "uid",
            b"uid",
        ],
    ) -> None: ...

global___GetBookCommentResult = GetBookCommentResult

class GetBookCommentListResult(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    RESULT_FIELD_NUMBER: builtins.int
    @property
    def result(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[
        global___GetBookCommentResult
    ]: ...
    def __init__(
        self,
        *,
        result: typing.Optional[typing.Iterable[global___GetBookCommentResult]] = ...,
    ) -> None: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["result", b"result"]
    ) -> None: ...

global___GetBookCommentListResult = GetBookCommentListResult
