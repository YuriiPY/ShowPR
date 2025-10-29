import { motion } from 'framer-motion'


import ChopstickIcon from '@/components/svgIcons/chopstick'
import DumplingIcon from '@/components/svgIcons/dumplingIcon'
import clsx from 'clsx'
import styles from './SmallLoadingWindow.module.scss'


export const SmallLoadingWindow = () => {
    return (
        <div className={styles.loadingContainer}>
            <motion.div
                className={clsx(styles.chopstickContainer, styles.firstIcon)}
                style={{ originX: 0.9, originY: 0 }}
                initial={{ rotate: 5 }}
                animate={{ rotate: [5, 0, -5] }}
                transition={{
                    duration: 1.5,
                    repeat: Infinity,
                    ease: "linear",
                    repeatType: "mirror"
                }}
            >
                <ChopstickIcon />
            </motion.div>
            <motion.div
                className={styles.dumplingContainer}
                initial={{ rotate: -10, x: "-50%", y: "-50%" }}
                animate={{ rotate: [-10, -5, 0, 5, 10] }}
                transition={{
                    duration: 1,
                    repeat: Infinity,
                    ease: "linear",
                    repeatType: "mirror"
                }}
            >
                <DumplingIcon />
            </motion.div>
            <motion.div
                className={clsx(styles.chopstickContainer, styles.secondIcon)}
                style={{ originX: 1, originY: 0.1 }}
                initial={{ rotate: -10 }}
                animate={{ rotate: [-10, -5, 0] }}
                transition={{
                    duration: 1.5,
                    repeat: Infinity,
                    ease: "linear",
                    repeatType: "mirror"
                }}
            >
                <ChopstickIcon />
            </motion.div>
        </div>
    )
}