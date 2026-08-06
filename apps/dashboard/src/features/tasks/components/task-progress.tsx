export function TaskProgress({
  progress,
}: {
  progress: number;
}) {
  const bounded = Math.min(
    Math.max(progress, 0),
    100,
  );

  return (
    <div>
      <div className="flex justify-between gap-3 text-xs">
        <span className="text-slate-500 dark:text-slate-400">
          Progress
        </span>

        <span className="font-semibold text-slate-700 dark:text-slate-300">
          {bounded}%
        </span>
      </div>

      <div className="mt-1.5 h-2 overflow-hidden rounded-full bg-slate-200 dark:bg-slate-700">
        <div
          className="h-full rounded-full bg-blue-600"
          style={{
            width: `${bounded}%`,
          }}
        />
      </div>
    </div>
  );
}
