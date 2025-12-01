import api from "./api";

/**
 * Enroll the logged-in user in a course.
 * Sends POST to /api/enrollments/courses/<course_id>/enroll/
 */
export async function enrollInCourse(courseId: number) {
  const response = await api.post(`/enrollments/courses/${courseId}/enroll/`);
  return response.data;
}
