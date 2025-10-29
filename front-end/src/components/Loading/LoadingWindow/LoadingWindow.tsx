"use client"

import { AnimatePresence, motion } from 'framer-motion'
import { useEffect, useRef, useState } from 'react'

import TransparentDumplingIcon from '../../svgIcons/transparentDumplingIcon'
import styles from './LoadingWindow.module.scss'

interface Point {
    x: number
    y: number
    opacity: number
}

let instanceMounted = false

export const LoadingWindow = () => {
    const [isLoading, setIsLoading] = useState(false)

    const canvasRef = useRef<HTMLCanvasElement | null>(null)
    const pointsRef1 = useRef<Point[]>([])
    const pointsRef2 = useRef<Point[]>([])

    useEffect(() => {

        if (instanceMounted) return
        instanceMounted = true

        const hasSeenLoadingWindow = sessionStorage.getItem("hasSeenLoadingWindow")

        if (hasSeenLoadingWindow) {
            setIsLoading(false)
        } else {
            setIsLoading(true)
            sessionStorage.setItem("hasSeenLoadingWindow", "true")
        }

        return () => {
            instanceMounted = false
        }

    }, [])

    useEffect(() => {
        const canvas = canvasRef.current
        if (!canvas) return
        const ctx = canvas.getContext('2d')
        if (!ctx) return

        let t = 0
        let animationFrameId: number

        const render = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height)

            const amplitude = 20
            const wavelength = 300
            const centerX = canvas.width / 2
            const speed = 0.5

            const newPoint1: Point = {
                x: centerX - 25 + Math.sin((t / wavelength) * 2 * Math.PI) * amplitude,
                y: canvas.height - 10,
                opacity: 1
            }

            const newPoint2: Point = {
                x: centerX + 25 + Math.cos((t / wavelength) * 2 * Math.PI) * amplitude,
                y: canvas.height,
                opacity: 1
            }

            t++

            // Рухаємо точки вгору і зменшуємо opacity
            pointsRef1.current = pointsRef1.current.map(p => ({
                x: p.x,
                y: p.y - speed,
                opacity: p.opacity - 0.003
            }))

            pointsRef2.current = pointsRef2.current.map(p => ({
                x: p.x,
                y: p.y - speed,
                opacity: p.opacity - 0.002
            }))

            // Додаємо нові точки
            pointsRef1.current.push(newPoint1)
            pointsRef2.current.push(newPoint2)

            // Ліміт точок
            if (pointsRef1.current.length > 500) pointsRef1.current.shift()
            if (pointsRef2.current.length > 500) pointsRef2.current.shift()

            // Малюємо першу хвилю
            for (let i = 1; i < pointsRef1.current.length; i++) {
                const prev = pointsRef1.current[i - 1]
                const curr = pointsRef1.current[i]

                ctx.beginPath()
                ctx.moveTo(prev.x, prev.y)
                ctx.lineTo(curr.x, curr.y)
                ctx.strokeStyle = `rgba(154, 154, 154, ${curr.opacity})`
                ctx.lineWidth = 8
                ctx.stroke()
            }

            // Малюємо другу хвилю
            for (let i = 1; i < pointsRef2.current.length; i++) {
                const prev = pointsRef2.current[i - 1]
                const curr = pointsRef2.current[i]

                ctx.beginPath()
                ctx.moveTo(prev.x, prev.y)
                ctx.lineTo(curr.x, curr.y)
                ctx.strokeStyle = `rgba(154, 154, 154, ${curr.opacity})`
                ctx.lineWidth = 8
                ctx.stroke()
            }

            // Очищаємо точки з opacity <= 0
            pointsRef1.current = pointsRef1.current.filter(p => p.opacity > 0)
            pointsRef2.current = pointsRef2.current.filter(p => p.opacity > 0)

            animationFrameId = requestAnimationFrame(render)
        }

        render()

        return () => cancelAnimationFrame(animationFrameId)
    }, [isLoading])

    useEffect(() => {
        if (isLoading) document.body.style.overflow = 'hidden'
    }, [isLoading])

    return (
        <AnimatePresence
            onExitComplete={() => {
                document.body.style.overflow = ''
            }}
        >
            {isLoading && (
                <motion.div
                    className={styles.loadingWindow}
                    initial={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.5 }}
                >
                    <div className={styles.backgroundOverlay}></div>
                    <div className={styles.container}>
                        <div className={styles.canvasContainer}>
                            <canvas ref={canvasRef} width={400} height={300} />
                        </div>
                        <div className={styles.loadingLogoContainer}>
                            <motion.div
                                initial={{ rotate: -10 }}
                                animate={{ rotate: [-10, -5, 0, 5, 10] }}
                                transition={{
                                    duration: .7,
                                    repeat: Infinity,
                                    ease: "linear",
                                    repeatType: "mirror"
                                }}
                            >
                                <TransparentDumplingIcon size={200} />
                            </motion.div>
                        </div>
                        <div className={styles.statusBarContainer}>
                            <motion.div
                                className={styles.statusBar}
                                initial={{ width: 0 }}
                                animate={{ width: ['10%', '20%', '50%', '55%', '70%', '80%', '90%', '100%'] }}
                                transition={{
                                    duration: 5,
                                    ease: "linear",
                                }}
                                onAnimationComplete={() => setIsLoading(false)}
                            >

                            </motion.div>
                        </div>
                    </div>
                </motion.div>
            )
            }
        </AnimatePresence >
    )
}
