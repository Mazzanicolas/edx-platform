# pylint: disable=unused-import,wildcard-import
"""
Python APIs exposed by the grades app to other in-process apps.
"""

# Public Grades Factories
from lms.djangoapps.grades.course_grade_factory import CourseGradeFactory
from lms.djangoapps.grades.subsection_grade_factory import SubsectionGradeFactory

# Public Grades Functions
from lms.djangoapps.grades.models_api import *
from lms.djangoapps.grades.tasks import compute_all_grades_for_course as task_compute_all_grades_for_course

# Public Grades Modules
from lms.djangoapps.grades import events, constants, context, course_data
from lms.djangoapps.grades.signals import signals
from lms.djangoapps.grades.util_services import GradesUtilService

# TODO exposing functionality from Grades handlers seems fishy.
from lms.djangoapps.grades.signals.handlers import disconnect_submissions_signal_receiver

# Grades APIs that should NOT belong within the Grades subsystem
# TODO move Gradebook to be an external feature outside of core Grades
from lms.djangoapps.grades.config.waffle import is_writable_gradebook_enabled


def graded_subsections_for_course_id(course_id):
    from lms.djangoapps.grades.context import graded_subsections_for_course
    return graded_subsections_for_course(course_data.CourseData(user=None, course_key=course_id).collected_structure)


def create_or_update_subsection_grade(
            course_id,
            block_id,
            student,
            grading_user,
            feature=constants.GradeOverrideFeatureEnum.gradebook,
            **override_data):
    try:
        subsection_grade_model = _PersistentSubsectionGrade.objects.get(
            user_id=student.id,
            course_id=course_id,
            usage_key=block_id
        )
    except _PersistentSubsectionGrade.DoesNotExist:
        from lms.djangoapps.grades.course_data import CourseData
        from lms.djangoapps.grades.subsection_grade import CreateSubsectionGrade
        course_data = CourseData(student, course_key=course_id)
        subsection_grade = CreateSubsectionGrade(subsection, course_data.structure, {}, {})
        subsection_grade_model = subsection_grade.update_or_create_model(student, force_update_subsections=True)

    override = _PersistentSubsectionGradeOverride.update_or_create_override(
        requesting_user=grading_user,
        subsection_grade_model=subsection_grade_model,
        feature=feature,
        **override_data
    )

    # set_event_transaction_type(events.SUBSECTION_GRADE_CALCULATED)
    # create_new_event_transaction_id()

    # recalculate_subsection_grade_v3.apply(
    #     kwargs=dict(
    #         user_id=subsection_grade_model.user_id,
    #         anonymous_user_id=None,
    #         course_id=text_type(subsection_grade_model.course_id),
    #         usage_id=text_type(subsection_grade_model.usage_key),
    #         only_if_higher=False,
    #         expected_modified_time=to_timestamp(override.modified),
    #         score_deleted=False,
    #         event_transaction_id=six.text_type(get_event_transaction_id()),
    #         event_transaction_type=six.text_type(get_event_transaction_type()),
    #         score_db_table=grades_constants.ScoreDatabaseTableEnum.overrides,
    #         force_update_subsections=True,
    #     )
    # )
    # Emit events to let our tracking system to know we updated subsection grade
    events.subsection_grade_calculated(subsection_grade_model)


