"use client"
import { routing } from '@/i18n/routing'
import clsx from 'clsx'
import { useLocale, useTranslations } from 'next-intl'
import Image from 'next/image'
import { usePathname, useRouter } from "next/navigation"
import { useState } from 'react'
import styles from './LanguageSelector.module.scss'

export function LanguageSelector() {
    const locale = useLocale()
    const router = useRouter()

    const pathname = usePathname()

    const t = useTranslations("TextForScreenReader.languageSelector")


    const handleSelectorChange = (e: string) => {
        const selectedValue = e

        const segments = pathname.split('/')
        segments[1] = selectedValue
        const newPath = segments.join('/')

        router.replace(newPath)
    }

    const [isSelectorOpen, setIsSelectorOpen] = useState(false)

    return (
        <div className={clsx(styles.languageSelector, { [styles.opened]: isSelectorOpen })}>
            <div className={styles.languageMainButton}>
                <button
                    onClick={() => {
                        setIsSelectorOpen((prev) => (!prev))
                    }}
                    aria-haspopup="listbox"
                    aria-expanded={isSelectorOpen}
                    aria-label={t("mainButtonLabel")}
                >
                    <Image src={`/icons/flags/${locale}.svg`} alt={""} width={20} height={20} />
                    {locale}
                </button>
            </div>
            <div className={clsx(styles.dropdown, { [styles.opened]: isSelectorOpen })}

                role='listbox'
                aria-label=""
            >
                {
                    routing.locales.map((lang) => (
                        <button
                            key={lang}
                            onClick={() => {
                                handleSelectorChange(lang)
                            }}
                            className={styles.dropdownItemButton}
                            role="option"
                            aria-label={lang + " " + t("language")}
                            aria-selected={locale === lang}
                        >
                            <Image src={`/icons/flags/${lang}.svg`} alt={t("flagAlt")} width={20} height={20} />
                            <span>{lang}</span>
                        </button>
                    ))
                }
            </div>
        </div >
    )
}