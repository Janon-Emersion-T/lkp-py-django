from django.db import transaction

from apps.activity.services import log_activity
from apps.audit.models import AuditEventType
from apps.audit.services import log_audit_event

from .models import (
    Team,
    TeamMember,
    TeamMembership,
    TeamMemberService,
)


class TeamManagementService:
    @staticmethod
    def team_snapshot(team):
        return {
            "id": str(team.id),
            "name": team.name,
            "slug": team.slug,
            "team_type": team.team_type,
            "parent_id": (
                str(team.parent_id)
                if team.parent_id
                else None
            ),
            "manager_id": (
                str(team.manager_id)
                if team.manager_id
                else None
            ),
            "is_active": team.is_active,
            "is_public": team.is_public,
            "sort_order": team.sort_order,
        }

    @staticmethod
    def member_snapshot(member):
        return {
            "id": str(member.id),
            "user_id": (
                str(member.user_id)
                if member.user_id
                else None
            ),
            "employee_code": member.employee_code,
            "first_name": member.first_name,
            "last_name": member.last_name,
            "job_title": member.job_title,
            "employment_status": (
                member.employment_status
            ),
            "engagement_type": member.engagement_type,
            "reports_to_id": (
                str(member.reports_to_id)
                if member.reports_to_id
                else None
            ),
            "is_public": member.is_public,
            "is_featured": member.is_featured,
        }

    @classmethod
    @transaction.atomic
    def create_team(
        cls,
        *,
        request,
        values,
    ):
        team = Team(**values)
        team.full_clean()
        team.save()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="team_management",
            message="Team created.",
            target_type="team_management.Team",
            target_id=str(team.pk),
            metadata={
                "after": cls.team_snapshot(team),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="create_team",
            module="team_management",
            description=f"Created team {team.name}.",
            entity_type="team_management.Team",
            entity_id=str(team.pk),
        )

        return team

    @classmethod
    @transaction.atomic
    def update_team(
        cls,
        *,
        request,
        team,
        values,
    ):
        before = cls.team_snapshot(team)

        for field, value in values.items():
            setattr(team, field, value)

        team.full_clean()
        team.save()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="team_management",
            message="Team updated.",
            target_type="team_management.Team",
            target_id=str(team.pk),
            metadata={
                "before": before,
                "after": cls.team_snapshot(team),
            },
        )

        return team

    @classmethod
    @transaction.atomic
    def create_member(
        cls,
        *,
        request,
        values,
        memberships,
        services,
    ):
        member = TeamMember(**values)
        member.full_clean()
        member.save()

        for membership in memberships:
            item = TeamMembership(
                member=member,
                **membership,
            )
            item.full_clean()
            item.save()

        for service in services:
            assignment = TeamMemberService(
                member=member,
                **service,
            )
            assignment.full_clean()
            assignment.save()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="team_management",
            message="Team member created.",
            target_type="team_management.TeamMember",
            target_id=str(member.pk),
            metadata={
                "after": cls.member_snapshot(member),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="create_team_member",
            module="team_management",
            description=(
                f"Created team member "
                f"{member.display_name}."
            ),
            entity_type="team_management.TeamMember",
            entity_id=str(member.pk),
        )

        return member

    @classmethod
    @transaction.atomic
    def update_member(
        cls,
        *,
        request,
        member,
        values,
        memberships,
        services,
    ):
        before = cls.member_snapshot(member)

        for field, value in values.items():
            setattr(member, field, value)

        member.full_clean()
        member.save()

        TeamMembership.objects.filter(
            member=member,
        ).delete()

        TeamMemberService.objects.filter(
            member=member,
        ).delete()

        for membership in memberships:
            item = TeamMembership(
                member=member,
                **membership,
            )
            item.full_clean()
            item.save()

        for service in services:
            assignment = TeamMemberService(
                member=member,
                **service,
            )
            assignment.full_clean()
            assignment.save()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="team_management",
            message="Team member updated.",
            target_type="team_management.TeamMember",
            target_id=str(member.pk),
            metadata={
                "before": before,
                "after": cls.member_snapshot(member),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="update_team_member",
            module="team_management",
            description=(
                f"Updated team member "
                f"{member.display_name}."
            ),
            entity_type="team_management.TeamMember",
            entity_id=str(member.pk),
        )

        return member


    @classmethod
    @transaction.atomic
    def update_member_status(
        cls,
        *,
        request,
        member,
        employment_status,
        employment_ended_at=None,
    ):
        before = cls.member_snapshot(member)

        member.employment_status = employment_status
        member.employment_ended_at = (
            employment_ended_at
        )

        member.full_clean()
        member.save(
            update_fields=[
                "employment_status",
                "employment_ended_at",
                "updated_at",
            ]
        )

        if employment_status not in {
            "active",
            "on_leave",
        }:
            TeamMembership.objects.filter(
                member=member,
                is_active=True,
            ).update(
                is_active=False,
            )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="team_management",
            message="Team member status updated.",
            target_type="team_management.TeamMember",
            target_id=str(member.pk),
            metadata={
                "before": before,
                "after": cls.member_snapshot(member),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="update_team_member_status",
            module="team_management",
            description=(
                f"Updated employment status for "
                f"{member.display_name}."
            ),
            entity_type="team_management.TeamMember",
            entity_id=str(member.pk),
        )

        return member

    @classmethod
    @transaction.atomic
    def update_reporting_line(
        cls,
        *,
        request,
        member,
        reports_to,
    ):
        before = cls.member_snapshot(member)

        member.reports_to = reports_to
        member.full_clean()
        member.save(
            update_fields=[
                "reports_to",
                "updated_at",
            ]
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="team_management",
            message="Team reporting line updated.",
            target_type="team_management.TeamMember",
            target_id=str(member.pk),
            metadata={
                "before": before,
                "after": cls.member_snapshot(member),
            },
        )

        return member

    @classmethod
    @transaction.atomic
    def set_team_manager(
        cls,
        *,
        request,
        team,
        manager,
    ):
        if manager is not None:
            membership = (
                TeamMembership.objects.filter(
                    team=team,
                    member=manager,
                    is_active=True,
                    is_deleted=False,
                ).first()
            )

            if membership is None:
                raise ValueError(
                    "The selected manager must be an "
                    "active member of the team."
                )

            if not membership.is_primary:
                TeamMembership.objects.filter(
                    member=manager,
                    is_primary=True,
                    is_active=True,
                    is_deleted=False,
                ).exclude(
                    pk=membership.pk,
                ).update(
                    is_primary=False,
                )

                membership.is_primary = True
                membership.save(
                    update_fields=[
                        "is_primary",
                        "updated_at",
                    ]
                )

        before = cls.team_snapshot(team)

        team.manager = manager
        team.save(
            update_fields=[
                "manager",
                "updated_at",
            ]
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="team_management",
            message="Team manager updated.",
            target_type="team_management.Team",
            target_id=str(team.pk),
            metadata={
                "before": before,
                "after": cls.team_snapshot(team),
            },
        )

        return team
