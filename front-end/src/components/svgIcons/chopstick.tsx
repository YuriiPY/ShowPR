import React from "react"

interface SVGIconProps {
    color?: string
    size?: number | string
    isOpen?: boolean
}

const ChopstickIcon: React.FC<SVGIconProps> = ({
    size = "100%"
}) => {

    return (
        <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 234 234"
            fill="none"
            width={size}
            height={size}
            x="0px" y="0px"
        >
            <path d="M213.187 3.27209C219.042 3.46058 230.457 14.8754 231.317 21.4015C232.177 27.9276 16.9667 226.351 13.5358 225.753C10.1049 225.155 8.76193 223.812 8.1641 220.381C7.56627 216.95 207.332 3.0836 213.187 3.27209Z" fill="black" />
            <rect x="194.771" y="20.2041" width="28" height="12" transform="rotate(45 194.771 20.2041)" fill="white" />
            <rect x="182.043" y="32.9321" width="28" height="12" transform="rotate(45 182.043 32.9321)" fill="white" />

        </svg>
    )
}

export default ChopstickIcon