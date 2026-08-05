import {
  CheckCircle2,
  CircleDashed,
  Database,
  KeyRound,
  LayoutDashboard,
  ShieldCheck,
} from "lucide-react";

import { PageHeader } from "../../components/layout/page-header";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "../../components/ui/card";
import { useAuth } from "../../features/auth/use-auth";

const moduleSummaries = [
  {
    label: "CRM",
    description: "Lead and client management will be introduced in a later milestone.",
  },
  {
    label: "Projects",
    description: "Project delivery and work tracking are not configured yet.",
  },
  {
    label: "Finance",
    description: "Financial reporting will be enabled after the core operational modules.",
  },
  {
    label: "Website CMS",
    description: "Website content management will be connected in its dedicated milestone.",
  },
] as const;

const foundationProgress = [
  {
    label: "Project foundation",
    complete: true,
  },
  {
    label: "Authentication",
    complete: true,
  },
  {
    label: "Protected routing",
    complete: true,
  },
  {
    label: "Dashboard layout",
    complete: false,
  },
  {
    label: "Roles and permissions",
    complete: false,
  },
] as const;

export function DashboardPage() {
  const { user } = useAuth();

  const displayName =
    [user?.first_name, user?.last_name]
      .filter(Boolean)
      .join(" ") || user?.email || "Administrator";

  return (
    <section className="space-y-8">
      <PageHeader
        eyebrow="Overview"
        title={`Welcome, ${displayName}`}
        description="This workspace will become the central operating platform for LKProfessionals. Business modules will be activated progressively as each milestone is completed."
      />

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {moduleSummaries.map((module) => (
          <Card key={module.label}>
            <CardHeader>
              <div className="mb-3 grid h-10 w-10 place-items-center rounded-lg bg-slate-100 text-slate-600">
                <CircleDashed size={20} />
              </div>

              <CardTitle>{module.label}</CardTitle>
            </CardHeader>

            <CardContent>
              <p className="text-sm leading-6 text-slate-500">
                {module.description}
              </p>

              <p className="mt-4 text-xs font-semibold uppercase tracking-wider text-slate-400">
                Not yet available
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.4fr_1fr]">
        <Card>
          <CardHeader>
            <CardTitle>Platform setup progress</CardTitle>
          </CardHeader>

          <CardContent>
            <div className="space-y-4">
              {foundationProgress.map((item) => (
                <div
                  key={item.label}
                  className="flex items-center justify-between gap-4 rounded-lg border border-slate-200 px-4 py-3"
                >
                  <div className="flex min-w-0 items-center gap-3">
                    {item.complete ? (
                      <CheckCircle2
                        size={18}
                        className="shrink-0 text-emerald-600"
                      />
                    ) : (
                      <CircleDashed
                        size={18}
                        className="shrink-0 text-slate-400"
                      />
                    )}

                    <span className="truncate text-sm font-medium text-slate-800">
                      {item.label}
                    </span>
                  </div>

                  <span
                    className={
                      item.complete
                        ? "text-xs font-semibold text-emerald-700"
                        : "text-xs font-semibold text-slate-400"
                    }
                  >
                    {item.complete ? "Complete" : "Pending"}
                  </span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <div className="mb-3 grid h-10 w-10 place-items-center rounded-lg bg-blue-50 text-blue-700">
                <ShieldCheck size={20} />
              </div>

              <CardTitle>Next milestone</CardTitle>
            </CardHeader>

            <CardContent>
              <p className="text-lg font-semibold text-slate-950">
                Roles and Permissions
              </p>

              <p className="mt-2 text-sm leading-6 text-slate-500">
                The next phase will establish role-based access control before operational modules are opened to additional users.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>System status</CardTitle>
            </CardHeader>

            <CardContent className="space-y-3">
              <div className="flex items-center gap-3 text-sm text-slate-700">
                <KeyRound size={17} className="text-emerald-600" />
                Authentication operational
              </div>

              <div className="flex items-center gap-3 text-sm text-slate-700">
                <LayoutDashboard size={17} className="text-emerald-600" />
                Protected dashboard operational
              </div>

              <div className="flex items-center gap-3 text-sm text-slate-700">
                <Database size={17} className="text-slate-400" />
                Business data modules pending
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
}
