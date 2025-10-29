import { PanelTopOpen } from 'lucide-react'

import clsx from 'clsx'
import { useState } from 'react'
import styles from './HoursTable.module.scss'

// type TableRow = {
//     day: string
//     hours: string
// }

type HoursTableProps = {
    title: string
    rows: Array<{ day: string, hours: string }>
}

export default function HoursTable({ title, rows }: HoursTableProps) {

    const [isTableOpen, setIsTableOpen] = useState(false)

    const handleOpenBtn = () => {
        setIsTableOpen(!isTableOpen)
    }

    const today = new Date()
    const dayIndex = today.getDay()

    return (
        <div className={styles.openingHours}>
            <div className={styles.openingHoursContainer}>
                <div className={styles.hoursTitle}>
                    <h2> {title}</h2 >
                    <button className={styles.limitsBtn} onClick={handleOpenBtn}>
                        < PanelTopOpen />
                    </button >
                </div>
                <div>
                    <table>
                        <tbody>
                            <tr>
                                <th className={styles.leftColumn}>Today:</th>
                                <td className={styles.spacer}></td>
                                <th className={styles.rightColumn}>{
                                    dayIndex === 0 ? "Close" :
                                        dayIndex === 6 ? "8:00 - 15:00" :
                                            "8:00 - 17:00"
                                }
                                </th>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div className={clsx(styles.workingHours, { [styles.visible]: isTableOpen })}>
                <div className={styles.workingHoursItem}>
                    <div className={styles.limitsTable}>
                        <table>
                            <tbody>
                                {rows.map((row, index) => (
                                    <tr key={index}>
                                        <th className={styles.leftColumn}>{row.day}</th>
                                        <td className={styles.spacer}></td>
                                        <th className={styles.rightColumn}>{row.hours}</th>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div >
    )
}