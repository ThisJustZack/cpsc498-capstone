import graphene
from graphene_django import DjangoObjectType

from database.models import *
from django.contrib.auth import get_user_model
from backend.api.schema_types import *
	
class Query(graphene.ObjectType):
	# User from Session Queries
	whoami = graphene.Field(UserType)
	created_courses = graphene.List(CourseType)
	learning_blocks_for_user = graphene.List(LearningBlockProgressType)
	watched_courses = graphene.List(WatchCourseType)
	favorited_courses = graphene.List(FavoriteCourseType)
	enrolled_courses = graphene.List(EnrolledCourseType)
	learning_blocks_for_user_from_course = graphene.List(LearningBlockProgressType, course_id=graphene.Int())

	# Ambiguous Queries
	user_from_id = graphene.Field(UserType, user_id=graphene.Int())
	courses_created_by_user = graphene.List(CourseType, user_id=graphene.Int())
	course_from_id = graphene.Field(CourseType, course_id=graphene.Int())
	units_from_course = graphene.List(UnitType, course_id=graphene.Int())
	subunits_from_unit = graphene.List(SubUnitType, unit_id=graphene.Int())
	learning_blocks_from_subunit = graphene.List(LearningBlockType, subunit_id=graphene.Int())
	
	# Search Queries
	search_courses = graphene.List(CourseType, search_text=graphene.String())
	
	# Session Resolvers (User)
	def resolve_whoami(root, info):
		if (info.context.user.is_anonymous):
			return None
		return info.context.user

	def resolve_created_courses(root, info):
		if (info.context.user.is_anonymous):
			return None
		return get_user_model().objects.get(pk=info.context.user.id).creations.all()

	def resolve_learning_blocks_for_user(root, info):
		if (info.context.user.is_anonymous):
			return None
		return get_user_model().objects.get(pk=info.context.user.id).user_progress.all()

	def resolve_watched_courses(root, info):
		if (info.context.user.is_anonymous):
			return None
		return get_user_model().objects.get(pk=info.context.user.id).watching.all()

	def resolve_favorited_courses(root, info):
		if (info.context.user.is_anonymous):
			return None
		return get_user_model().objects.get(pk=info.context.user.id).favorited.all()

	def resolve_enrolled_courses(root, info):
		if (info.context.user.is_anonymous):
			return None
		return get_user_model().objects.get(pk=info.context.user.id).enrolled.all()

	def resolve_learning_blocks_for_user_from_course(root, info, course_id):
		if (info.context.user.is_anonymous):
			return None
		return None

	# Ambiguous Resolvers
	def resolve_user_from_id(root, info, user_id):
		try:
			return get_user_model().objects.get(pk=user_id)
		except User.DoesNotExist:
			return None

	def resolve_courses_created_by_user(root, info, user_id):
		try:
			return get_user_model().objects.get(pk=user_id).creations.all()
		except get_user_model().DoesNotExist:
			return None

	def resolve_learning_block_progress_for_user_from_course(root, info, user_id, course_id):
		try:
			user_instance = get_user_model().objects.get(pk=user_id)
			return None
		except get_user_model().DoesNotExist:
			return None

	def resolve_course_from_id(root, info, course_id):
		try: 
			return Course.objects.get(pk=course_id)
		except Course.DoesNotExist:
			return None
	
	def resolve_units_from_course(root, info, course_id):
		try: 
			return Course.objects.get(pk=course_id).units.all()
		except Course.DoesNotExist:
			return None

	def resolve_subunits_from_unit(root, info, unit_id):
		try: 
			return Unit.objects.get(pk=unit_id).subunits.all()
		except Unit.DoesNotExist:
			return None

	def resolve_learning_blocks_from_subunit(root, info, subunit_id):
		try: 
			return SubUnit.objects.get(pk=subunit_id).learning_blocks.all()
		except SubUnit.DoesNotExist:
			return None

	# Search Resolvers
	def resolve_search_courses(root, info, search_text):
		try: 
			return Course.objects.filter(name__icontains=search_text)
		except Course.DoesNotExist:
			return None