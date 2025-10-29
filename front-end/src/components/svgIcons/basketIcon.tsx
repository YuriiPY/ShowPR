import { motion } from "framer-motion"
import React from "react"

interface SVGIconProps {
    color?: string
    size?: number
    isOpen?: boolean
}

const BasketIcon: React.FC<SVGIconProps> = ({
    size = 50,
    isOpen = false
}) => {

    const leftHandleVariants = {
        closed: { d: "M5 11L9 4" },
        open: { d: "M5 11L2 4" },
    }

    const rightHandleVariants = {
        closed: { d: "M19 11L15 4" },
        open: { d: "M19 11L22 4" },
    }

    return (
        <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            width={size}
            height={size}
        >
            <path d="M4 12H20L19.5 19H4.5L4 12Z" fill="white" />
            <path d="M15 11L14 20" stroke="black" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            <path d="M2 11H22" stroke="black" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            <path d="M3.5 11L5.1 18.4C5.1935 18.8586 5.44485 19.2698 5.81028 19.5621C6.17572 19.8545 6.63211 20.0094 7.1 20H16.9C17.3679 20.0094 17.8243 19.8545 18.1897 19.5621C18.5552 19.2698 18.8065 18.8586 18.9 18.4L20.6 11" stroke="black" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            <path d="M4.5 15.5H19.5" stroke="black" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            <path d="M9 11L10 20" stroke="black" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />


            <motion.path
                variants={leftHandleVariants}
                initial={isOpen ? "open" : "closed"}
                animate={isOpen ? "open" : "closed"}
                stroke="black"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                transition={{ duration: 0.3 }}
            />

            <motion.path
                variants={rightHandleVariants}
                initial={isOpen ? "open" : "closed"}
                animate={isOpen ? "open" : "closed"}
                stroke="black"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                transition={{ duration: 0.3 }}
            />
        </svg>
    )
}

export default BasketIcon