interface ProjectProgressProps {
  progress: number;
  compact?: boolean;
}

export function ProjectProgress({
  progress,
  compact = false,
}: ProjectProgressProps) {
  const boundedProgress = Math.min(
    Math.max(progress, 0),
    100,
  );

  return (
    <div className="min-w-28">
      <div className="flex items-center justify-between gap-3">
        {!compact && (
          <span className="text-xs text-slate-500 dark:text-slate-400">
            Progress
          </span>
        )}

        <span className="ml-auto text-xs font-semibold text-slate-700 dark:text-slate-300">
          {boundedProgress}%
        </span>
      </div>

      <div className="mt-1.5 h-2 overflow-hidden rounded-full bg-slate-200 dark:bg-slate-700">
        <div
          className="h-full rounded-full bg-blue-600 transition-[width]"
          style={{
            width: `${boundedProgress}%`,
          }}
        />
      </div>
    </div>
  );
}
