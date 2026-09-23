import { TopNav } from "@/components/top-nav";
import { WorkspaceClient } from "@/components/workspace/workspace-client";

export default async function LessonPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return (
    <div className="min-h-screen">
      <TopNav />
      <WorkspaceClient lessonId={id} />
    </div>
  );
}
