import React from 'react'

import { ChevronDown, ChevronUp } from 'lucide-react'

import styles from './TimePeakier.module.scss'

type Timer = {
    hours: number,
    minutes: number
}

type TimerAction =
    | { type: "increment" | "decrement", field: "hours" }
    | { type: "increment" | "decrement", field: "minutes" }
    | { type: "update", field: Timer }

interface TimePeakierProps {
    timeData: Timer
    setTimeData: React.Dispatch<TimerAction>
}

const TimePeakier = React.memo(({ timeData, setTimeData }: TimePeakierProps) => {

    return (
        <>
            <div className={styles.timePeakier}>
                <div className={styles.container}>
                    <div className={styles.row}>
                        <div className={styles.timePeakierBtn}>
                            <button
                                type='button'
                                onClick={() => {
                                    setTimeData({ type: "increment", field: "hours" })
                                }}
                            >
                                <span>
                                    <ChevronUp />
                                </span>
                            </button>
                            <button
                                type='button'
                                onClick={() => {
                                    setTimeData({ type: "increment", field: "minutes" })
                                }}
                            >
                                <span>
                                    <ChevronUp />
                                </span>
                            </button>
                        </div>
                        <div className={styles.timeContent}>
                            <input
                                value={
                                    timeData.hours.toString().length === 2
                                        ? timeData.hours
                                        : `0${timeData.hours}`
                                }
                                type='text'
                                name='deliveryTimeHour'
                                readOnly
                                className={styles.formTimeControl}
                            />
                            {":"}
                            <input
                                value={
                                    timeData.minutes.toString().length === 2
                                        ? timeData.minutes
                                        : `0${timeData.minutes}`
                                }
                                type='text'
                                name='deliveryTimeHour'
                                readOnly
                                className={styles.formTimeControl}
                            />
                        </div>
                        <div className={styles.timePeakierBtn}>
                            <button
                                type='button'
                                onClick={() => {
                                    setTimeData({ type: "decrement", field: "hours" })
                                }}
                            >
                                <span>
                                    <ChevronDown />
                                </span>
                            </button>
                            <button
                                type='button'
                                onClick={() => {
                                    setTimeData({ type: "decrement", field: "minutes" })
                                }}
                            >
                                <span>
                                    <ChevronDown />
                                </span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
})

TimePeakier.displayName = "TimePeakier"

export default TimePeakier