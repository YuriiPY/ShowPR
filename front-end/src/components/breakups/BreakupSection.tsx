'use client'

import styles from './Breakups-styles.module.scss'

type SectionTypes = { type: "up" | "down" }

const BreakupStyles = {
	"up": styles.spaceSectionUp,
	"down": styles.spaceSectionDown
}

export default function BreakupSection({ type }: SectionTypes) {
	return (
		<section className={BreakupStyles[type]}>
			<div></div>
		</section>
	)
}