import { Outlet, createRootRoute } from "@tanstack/react-router";
import { NotFound } from "@/components/shared";

export const Route = createRootRoute({
	component: () => (
		<>
			<Outlet />
			{/*<TanStackRouterDevtools/>*/}
		</>
	),
	notFoundComponent: () => <NotFound text="Not Found" />,
});
