import { useAccount, useOwnedCourse } from "@components/hooks/web3";
import { useWeb3 } from "@components/providers";
import { Message, Modal } from "@components/ui/common";
import { CourseHero, Curriculum, Keypoints } from "@components/ui/course";
import { BaseLayout } from "@components/ui/layout";
import { getAllCourses } from "@content/courses/fetcher";

export default function Course({ course }) {
  const { isLoading } = useWeb3();
  const { account } = useAccount();
  const { ownedCourse } = useOwnedCourse(course, account.data);
  const courseState = ownedCourse.data?.state;

  const isLocked =
    !courseState ||
    courseState === "purchased" ||
    courseState === "deactivated";

  return (
    <>
      <div className="py-4">
        <CourseHero hasOwner={!!ownedCourse.data} course={course} />
      </div>
      <Keypoints course={course} />
      {courseState && (
        <div className="max-w-5xl mx-auto">
          {courseState === "purchased" && (
            <Message type="warning">
              Course is purchased and waiting for activation. Process can take
              up to 24 horus.
              <i className="block font-normal">
                Incase of any questions, please contact lucasrahn09@gmail.com
              </i>
            </Message>
          )}
          {courseState === "activated" && (
            <Message>Lucas wishes you happy watching.</Message>
          )}
          {courseState === "deactivated" && (
            <Message type="danger">
              Course has been deactivated due to incorrect purchase data. The
              functionality to watch the course has been temporarily disabled
              <i className="block font-normal">
                Please contact lucasrahn09@gmail.com
              </i>
            </Message>
          )}
        </div>
      )}

      <Curriculum
        isLoading={isLoading}
        locked={isLocked}
        courseState={courseState}
      />
      <Modal />
    </>
  );
}

Course.Layout = BaseLayout;

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
