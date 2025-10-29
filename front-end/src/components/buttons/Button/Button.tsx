'use client'

import { LucideProps } from 'lucide-react'
import Image from 'next/image'
import { ForwardRefExoticComponent, RefAttributes } from "react"

import clsx from 'clsx'
import { useRouter } from 'next/navigation'
import styles from './Button.module.scss'

type ButtonProps = {
    type: "elevated" | "text"
    buttonName?: string,
    buttonHover?: "underline" | "changeColor" | "none",
    color?: string,
    link?: string,
    icon?:
    | ForwardRefExoticComponent<Omit<LucideProps, 'ref'> & RefAttributes<SVGSVGElement>>
    | React.FC<React.SVGProps<SVGSVGElement>>
    | string
    | null
    iconSize?: number,
    onClick?: (...args: unknown[]) => void,
    args?: unknown[]
}

const ButtonStyles = {
    "elevated": styles.elevated,
    "text": styles.text,
}

const ButtonHoverStyles = {
    "underline": styles.underline,
    "changeColor": styles.changeColor,
    "none": ""

}
export default function Button({
    type,
    buttonName,
    buttonHover = "none",
    link,
    color,
    icon: Icon = null,
    iconSize = 24,
    onClick,
    args = []
}: ButtonProps) {
    const router = useRouter()

    const handleClick = () => {
        if (onClick) {
            onClick(...args)
        } else if (link) {
            router.push(link)
        }
    }

    return (

        <button className={clsx(styles.mainBtnStyle, ButtonStyles[type], ButtonHoverStyles[buttonHover], `${buttonName}`)} onClick={handleClick} >
            {Icon && (
                <span className={styles.buttonIcon}>
                    {typeof Icon === "string" ? (
                        <Image
                            src={Icon}
                            alt={`${buttonName} icon`}
                            width={iconSize}
                            height={iconSize}
                            style={{ width: iconSize, height: iconSize }}
                        />
                    ) : (
                        <Icon size={iconSize} />
                    )}
                </span>
            )}
            <style>{`
            .${buttonName} {
            color: ${color} !important;
            }
            .${buttonName}:hover {
            color: #000 !important;
            }
            `
            }</style>
            {buttonName}
        </button >
    )
}