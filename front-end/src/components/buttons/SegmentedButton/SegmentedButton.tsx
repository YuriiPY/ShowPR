'use client'


import clsx from 'clsx'
import { Check } from 'lucide-react'
import { usePathname, useRouter } from 'next/navigation'
import React, { useState } from 'react'
import styles from './SegmentedButton.module.scss'

type ButtonProps = {
    type: "outline" | "text"
    hoverType: "changeColor" | "changeBackColor" | "underline"
    selfSelect?: boolean
    selectType: "checkIcon" | "hoverStyle"
    buttonsList: Array<{
        buttonName: string
        link?: string
        onClick?: (...args: unknown[]) => void,
        args?: unknown[]
        isSelected?: boolean
    }>
}

const SegmentedButtonsStyles = {
    "outline": styles.outline,
    "text": styles.text,
}

const SegmentedButtonsHoverStyles = {
    "changeColor": styles.changeColor,
    "changeBackColor": styles.changeBackColor,
    "underline": styles.underline
}

function SegmentedButton({ type, hoverType, selfSelect = true, selectType, buttonsList }: ButtonProps) {
    const router = useRouter()
    const middleIndex = Math.floor(buttonsList.length / 2)

    const [selectedButtonId, setSelectedButtonId] = useState<number>(0)

    const firstPathName = usePathname()

    const pathName = firstPathName.slice(3) === ""
        ? "/"
        : firstPathName.slice(3)

    return (
        <div className={clsx(styles.buttonsContainer, SegmentedButtonsStyles[type])}>
            {
                buttonsList.map((item, index) => {
                    const isSelected = selfSelect ? index === selectedButtonId : item.isSelected

                    return (
                        <div key={index} className={clsx(styles.btnContainer, SegmentedButtonsHoverStyles[hoverType], {
                            [styles.middleElement]: index === middleIndex && buttonsList.length % 2 !== 0,
                            [styles.selected]: isSelected && selectType === "hoverStyle"
                        })}>
                            <button className={styles.segmentButton}
                                onClick={() => {

                                    if (selfSelect) {
                                        setSelectedButtonId(index)
                                    }
                                    if (item.link && !item.onClick) {
                                        if (item.link !== pathName) {
                                            router.push(item.link)
                                        } else {
                                            window.scrollTo({ top: 0, behavior: 'smooth' })
                                        }
                                    } else if (item.onClick) {
                                        item.onClick(...(item.args || []))
                                    }
                                }}
                            >
                                {
                                    isSelected && selectType === "checkIcon" &&
                                    <span className={styles.buttonIcon}>
                                        <Check size={20} />
                                    </span>
                                }
                                {item.buttonName}
                            </button>

                        </div>
                    )
                })
            }
        </div >
    )
}

export default React.memo(SegmentedButton)