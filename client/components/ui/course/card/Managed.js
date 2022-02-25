const Item = ({ title, value, className }) => (
  <div className={`${className} px-4 py-2 sm:px-6`}>
    <div className="text-sm font-medium text-gray-500">{title}</div>
    <div className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
      {value}
    </div>
  </div>
);

export default function ManagedCourseCard({ children, course }) {
  return (
    <div className="bg-white border shadow overflow-hidden sm:rounded-lg mb-3">
      <div className="border-t border-gray-200">
        {Object.keys(course).map((key, idx) => (
          <Item
            key={key}
            title={key[0].toUpperCase() + key.slice(1)}
            value={course[key]}
            className={`${idx % 2 ? "bg-grey-50" : "bg-white"}`}
          />
        ))}

        <div className="bg-white px-4 py-5 sm:px-6">{children}</div>
      </div>
    </div>
  );
}
