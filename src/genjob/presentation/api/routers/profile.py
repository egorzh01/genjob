from __future__ import annotations

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from genjob.application.usecases.add_education import (
    AddEducationUC,
    AddEducationUCRequest,
)
from genjob.application.usecases.add_experience import (
    AddExperienceUC,
    AddExperienceUCRequest,
)
from genjob.application.usecases.create_profile import (
    CreateProfileUC,
    CreateProfileUCRequest,
)
from genjob.application.usecases.delete_education import DeleteEducationUC
from genjob.application.usecases.delete_experience import DeleteExperienceUC
from genjob.application.usecases.delete_profile import DeleteProfileUC
from genjob.application.usecases.update_contacts import (
    UpdateContactsUC,
    UpdateContactsUCRequest,
)
from genjob.application.usecases.update_education import (
    UpdateEducationUC,
    UpdateEducationUCRequest,
)
from genjob.application.usecases.update_experience import (
    UpdateExperienceUC,
    UpdateExperienceUCRequest,
)
from genjob.domain.entities import ProfileEducationId, ProfileExperienceId, ProfileId
from genjob.presentation.api.presenters.profile import ProfilePresenter
from genjob.presentation.api.schemas.profile import (
    ProfileContactsSchema,
    ProfileEducationListSchema,
    ProfileEducationSchema,
    ProfileExperienceListSchema,
    ProfileExperienceSchema,
    ProfileListSchema,
    ProfileSchema,
)

router = APIRouter(
    route_class=DishkaRoute,
)


@router.get(
    "/profiles",
    response_model=ProfileListSchema,
)
async def get_profiles(
    presenter: FromDishka[ProfilePresenter],
) -> ProfileListSchema:
    return await presenter.get_profiles()


@router.post(
    "/profiles",
    response_model=ProfileSchema,
)
async def create_profile(
    presenter: FromDishka[ProfilePresenter],
    uc: FromDishka[CreateProfileUC],
    req: CreateProfileUCRequest,
) -> ProfileSchema:
    profile_id = await uc(req)
    return await presenter.get_profile(profile_id=profile_id)


@router.get(
    "/profiles/{profile_id}",
    response_model=ProfileSchema,
)
async def get_profile(
    presenter: FromDishka[ProfilePresenter],
    profile_id: ProfileId,
) -> ProfileSchema:
    return await presenter.get_profile(profile_id=profile_id)


@router.delete(
    "/profiles/{profile_id}",
)
async def delete_profile(
    profile_id: ProfileId,
    uc: FromDishka[DeleteProfileUC],
) -> None:
    await uc(profile_id=profile_id)


@router.get(
    "/profiles/{profile_id}/contacts",
    response_model=ProfileContactsSchema,
)
async def get_profile_contacts(
    presenter: FromDishka[ProfilePresenter],
    profile_id: ProfileId,
) -> ProfileContactsSchema:
    return await presenter.get_profile_contacts(profile_id=profile_id)


@router.patch(
    "/profiles/{profile_id}/contacts",
    response_model=ProfileContactsSchema,
)
async def save_profile_contacts(
    presenter: FromDishka[ProfilePresenter],
    profile_id: ProfileId,
    uc: FromDishka[UpdateContactsUC],
    req: UpdateContactsUCRequest,
) -> ProfileContactsSchema:
    await uc(profile_id=profile_id, req=req)
    return await presenter.get_profile_contacts(profile_id=profile_id)


@router.post(
    "/profiles/{profile_id}/educations",
    response_model=ProfileEducationSchema,
)
async def add_profile_education(
    presenter: FromDishka[ProfilePresenter],
    profile_id: ProfileId,
    uc: FromDishka[AddEducationUC],
    req: AddEducationUCRequest,
) -> ProfileEducationSchema:
    profile_education_id = await uc(profile_id=profile_id, req=req)
    return await presenter.get_profile_education(
        profile_education_id=profile_education_id,
    )


@router.get(
    "/profiles/{profile_id}/educations",
    response_model=ProfileEducationListSchema,
)
async def get_profile_educations(
    presenter: FromDishka[ProfilePresenter],
    profile_id: ProfileId,
) -> ProfileEducationListSchema:
    return await presenter.get_profile_educations(profile_id=profile_id)


@router.patch(
    "/educations/{profile_education_id}",
    response_model=ProfileEducationSchema,
)
async def update_profile_education(
    presenter: FromDishka[ProfilePresenter],
    profile_education_id: ProfileEducationId,
    uc: FromDishka[UpdateEducationUC],
    req: UpdateEducationUCRequest,
) -> ProfileEducationSchema:
    await uc(profile_education_id=profile_education_id, req=req)
    return await presenter.get_profile_education(
        profile_education_id=profile_education_id,
    )


@router.delete(
    "/educations/{profile_education_id}",
)
async def delete_profile_education(
    profile_education_id: ProfileEducationId,
    uc: FromDishka[DeleteEducationUC],
) -> None:
    await uc(profile_education_id=profile_education_id)


@router.post(
    "/profiles/{profile_id}/experiences",
    response_model=ProfileExperienceSchema,
)
async def add_profile_experience(
    presenter: FromDishka[ProfilePresenter],
    profile_id: ProfileId,
    uc: FromDishka[AddExperienceUC],
    req: AddExperienceUCRequest,
) -> ProfileExperienceSchema:
    profile_experience_id = await uc(profile_id=profile_id, req=req)
    return await presenter.get_profile_experience(
        profile_experience_id=profile_experience_id,
    )


@router.get(
    "/profiles/{profile_id}/experiences",
    response_model=ProfileExperienceListSchema,
)
async def get_profile_experiences(
    presenter: FromDishka[ProfilePresenter],
    profile_id: ProfileId,
) -> ProfileExperienceListSchema:
    return await presenter.get_profile_experiences(profile_id=profile_id)


@router.patch(
    "/experiences/{profile_experience_id}",
    response_model=ProfileExperienceSchema,
)
async def update_profile_experience(
    presenter: FromDishka[ProfilePresenter],
    profile_experience_id: ProfileExperienceId,
    uc: FromDishka[UpdateExperienceUC],
    req: UpdateExperienceUCRequest,
) -> ProfileExperienceSchema:
    await uc(profile_experience_id=profile_experience_id, req=req)
    return await presenter.get_profile_experience(
        profile_experience_id=profile_experience_id,
    )


@router.delete(
    "/experiences/{profile_experience_id}",
)
async def delete_profile_experience(
    profile_experience_id: ProfileExperienceId,
    uc: FromDishka[DeleteExperienceUC],
) -> None:
    await uc(profile_experience_id=profile_experience_id)
