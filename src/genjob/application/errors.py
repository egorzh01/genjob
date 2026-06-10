from __future__ import annotations


class AppError(Exception):
    status_code = 500
    code = "SERVER_ERROR"


class AuthCodeNotFoundError(AppError):
    status_code = 400
    code = "AUTH_CODE_NOT_FOUND"


class AuthCodeInvalidError(AppError):
    status_code = 400
    code = "AUTH_CODE_INVALID"


class UserNotFoundError(AppError):
    status_code = 404
    code = "USER_NOT_FOUND"


class ProfileEducationNotFoundError(AppError):
    status_code = 404
    code = "PROFILE_EDUCATION_NOT_FOUND"


class ProfileExperienceNotFoundError(AppError):
    status_code = 404
    code = "PROFILE_EXPERIENCE_NOT_FOUND"


class ProfileNotFoundError(AppError):
    status_code = 404
    code = "PROFILE_NOT_FOUND"


class ProfileContactsNotFoundError(AppError):
    status_code = 404
    code = "PROFILE_CONTACTS_NOT_FOUND"
