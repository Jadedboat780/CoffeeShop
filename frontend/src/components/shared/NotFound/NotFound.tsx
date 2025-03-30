import { CoffeeSpin } from "@/components/ui";
import { Link } from "@tanstack/react-router";
import type { FC } from "react";
import styles from "./NotFound.module.css";

type Props = {
	text: string;
};

export const NotFound: FC<Props> = ({ text }) => {
	return (
		<div className={styles.not_found}>
			<CoffeeSpin />
			<p className={styles.message}>{text}</p>
			<Link className={styles.go_home} to="/">
				Go home
			</Link>
		</div>
	);
};
