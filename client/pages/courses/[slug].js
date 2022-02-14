import { Modal } from "@components/ui/common";
import { CourseHero, Curriculum, Keypoints } from "@components/ui/course";
import { BaseLayout } from "@components/ui/layout";
import { getAllCourses } from "@content/courses/fetcher";

export default function Course({ course }) {
  return (
    <BaseLayout>
      <div className="py-4">
        <CourseHero course={course} />
      </div>
      <Keypoints course={course} />
      <Curriculum locked={true} />
      <Modal />
    </BaseLayout>
  );
}

export const getStaticPaths = () => {
  const { data } = getAllCourses();

  return {
    paths: data.map((course) => ({
      params: {
        slug: course.slug,
      },
    })),
    fallback: false,
  };
};

export const getStaticProps = ({ params }) => {
  const { data } = getAllCourses();
  const course = data.filter((course) => course.slug === params.slug)[0];

  return {
    props: {
      course,
    },
  };
};
