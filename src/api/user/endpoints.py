import logging
from http import HTTPStatus
from typing import Dict, Tuple

from flask import g, request
from flask_restx import Resource

from api.user import schemas
from helpers.api import auth
from helpers.responses import failure_response, success_response
from model.user import User

from . import api


@api.route("/")
class UserList(Resource):
    @api.doc("Add new user")
    @api.expect(schemas.user_expect, validate=True)
    @api.marshal_list_with(schemas.user_response, skip_none=True)
    def post(self) -> Tuple[Dict, int]:
        """
        Add new user

        Returns:
            User
        """
        api.logger.info("Create user")
        user = User.get_by_email(api.payload["email"])
        if user:
            return failure_response(["Cannot add a user."], HTTPStatus.BAD_REQUEST)

        user = User(**api.payload).insert()
        return success_response(user, HTTPStatus.CREATED)

    @api.doc("List users")
    @api.param("page")
    @api.param("per_page")
    @api.marshal_list_with(schemas.user_list_response, skip_none=True)
    def get(self) -> Tuple[Dict, int]:
        """
        Get all users

        Returns:
            List of users
        """
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=4, type=int)
        api.logger.info("List users")
        users = User.list(page=page, per_page=per_page)

        return success_response(users, HTTPStatus.OK)


@api.route("/<int:user_id>")
class UserItem(Resource):
    @api.doc("Get user by id")
    @api.marshal_list_with(schemas.user_response, skip_none=True)
    def get(self, user_id: int) -> Tuple[Dict, int]:
        """
        Get user by id

        Args:
            user_id: user id

        Returns:
            User
        """
        api.logger.info(f"Get a users with ID: {user_id}")
        user = User.get_by_id(user_id)
        if not user:
            return failure_response(["User does not exist."], HTTPStatus.NOT_FOUND)
        return success_response(user, HTTPStatus.OK)

    @api.doc("Delete user")
    @auth
    def delete(self, user_id: int) -> Tuple[dict, int]:
        """
        Delete user
        An authenticated user can delete any other user

        Returns:
            Failure or 204
        """
        api.logger.info("Delete user")
        user = User.get_by_id(user_id)
        if not user:
            return failure_response(["User does not exist."], HTTPStatus.NOT_FOUND)
        logging.info(g.user.email, " is deleting ", user.email)
        user.delete()
        return success_response(user, HTTPStatus.OK)
