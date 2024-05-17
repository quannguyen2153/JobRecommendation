export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="">
      <div className="w-full h-full">{children}</div>
    </div>
  );
}
