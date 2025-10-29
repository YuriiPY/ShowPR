'use client'

import clsx from 'clsx'
import { SquareArrowOutUpRight } from 'lucide-react'
import { useTranslations } from 'next-intl'
import Image from 'next/image'
import Link from 'next/link'

import BreakupSection from '../breakups/BreakupSection'
import Button from '../buttons/Button/Button'
import styles from './Footer.module.scss'


export default function Footer() {
    const t = useTranslations("Footer")
    return (
        <footer className={styles.primaryFooter}>
            <BreakupSection type='down' />
            <div className={styles.backgroundOverlay}></div>
            <div className={styles.backgroundFooterOverlayImg}></div>
            <div className={styles.elementSection}>
                <div className={styles.element}>
                    <div className={styles.elementContainer}>
                        <div className={styles.col33}>
                            <div className={styles.elementElement}>
                                <h1>{t("Column1.title")}</h1>
                            </div>
                            <div className={styles.elementElement}>
                                <div className={styles.elementPhoto}>
                                    <Image src="/icons/under-line.png" alt='' width={150} height={21} />
                                </div>
                            </div>
                            <div className={styles.elementElement}>
                                <ul className={styles.elementList}>
                                    <li className={styles.elementItem}>
                                        <span>Alina Pierogowa</span>
                                    </li>
                                    <li className={styles.elementItem}>
                                        <Link href="https://www.google.com/maps/place/Alina+Pierogowa/@51.1211566,17.0446063,17z/data=!4m6!3m5!1s0x470fe9f9a1132313:0x55b3d3ff7d2b4304!8m2!3d51.120992!4d17.04455!16s%2Fg%2F11f6626d37?entry=ttu">
                                            <span>ul.Oleśnicka 13, 50-320 Wrocław</span>
                                        </Link>
                                    </li>
                                    <li className={styles.elementItem}>
                                        <span>NIP: 889 278 31 81</span>
                                    </li>
                                    <li className={styles.elementItem}>
                                        <span>{t("Column1.bankAccount")}:</span>
                                    </li>
                                    <li className={styles.elementItem}>
                                        <span>71 1050 1585 9675 0000 5733</span>
                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div className={clsx(styles.col33, styles.middleElement)}>
                            <div className={styles.elementElement}>
                                <h1>{t("Column2.title")}</h1>
                            </div>
                            <div className={styles.elementElement}>
                                <div className={styles.elementPhoto}>
                                    <Image src="/icons/under-line.png" alt='' width={150} height={21} />
                                </div>
                            </div>
                            <div className={styles.elementElement}>
                                <table>
                                    <tbody>
                                        <tr>
                                            <th className={styles.leftColumn}>{t("Column2.workDays.mon")}</th>
                                            <td className={styles.spacer}></td>
                                            <th className={styles.rightColumn}>8:00 - 17:00</th>
                                        </tr>
                                        <tr>
                                            <th className={styles.leftColumn}>{t("Column2.workDays.tue")}</th>
                                            <td className={styles.spacer}></td>
                                            <th className={styles.rightColumn}>8:00 - 17:00</th>
                                        </tr>
                                        <tr>
                                            <th className={styles.leftColumn}>{t("Column2.workDays.wed")}</th>
                                            <td className={styles.spacer}></td>
                                            <th className={styles.rightColumn}>8:00 - 17:00</th>
                                        </tr>
                                        <tr>
                                            <th className={styles.leftColumn}>{t("Column2.workDays.thu")}</th>
                                            <td className={styles.spacer}></td>
                                            <th className={styles.rightColumn}>8:00 - 17:00</th>
                                        </tr>
                                        <tr>
                                            <th className={styles.leftColumn}>{t("Column2.workDays.fri")}</th>
                                            <td className={styles.spacer}></td>
                                            <th className={styles.rightColumn}>8:00 - 17:00</th>
                                        </tr>
                                        <tr>
                                            <th className={styles.leftColumn}>{t("Column2.workDays.sat")}</th>
                                            <td className={styles.spacer}></td>
                                            <th className={styles.rightColumn}>8:00 - 15:00</th>
                                        </tr>
                                        <tr>
                                            <th className={styles.leftColumn}>{t("Column2.workDays.sun")}</th>
                                            <td className={styles.spacer}></td>
                                            <th className={styles.rightColumn}>{t("Column2.closed")}</th>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        <div className={styles.col33}>
                            <div className={styles.elementElement}>
                                <h1>{t("Column3.title")}</h1>
                            </div>
                            <div className={styles.elementElement}>
                                <div className={styles.elementPhoto}>
                                    <Image src="/icons/under-line.png" alt='' width={150} height={21} />
                                </div>
                            </div>
                            <div className={styles.elementElement}>
                                <ul className={styles.elementList}>
                                    <li className={styles.elementItemNav}>
                                        <Button color='#ffffff' type='text' buttonName={t("Column3.linksName.home")} link='/' icon={SquareArrowOutUpRight} />
                                    </li>
                                    <li className={styles.elementItemNav}>
                                        <Button color='#ffffff' type='text' buttonName={t("Column3.linksName.contacts")} link='/contacts' icon={SquareArrowOutUpRight} />
                                    </li>
                                    <li className={styles.elementItemNav}>
                                        <Button color='#ffffff' type='text' buttonName={t("Column3.linksName.menu")} link='/Menu' icon={SquareArrowOutUpRight} />
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </footer>
    )
}
