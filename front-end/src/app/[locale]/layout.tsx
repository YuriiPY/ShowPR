import type { Metadata } from 'next'
import React from 'react'

import Footer from '@/components/Footer/Footer'
import QueryProvider from '@/components/QueryProvider/QueryProvider'
import { NextIntlClientProvider, hasLocale } from 'next-intl'
import { notFound } from 'next/navigation'
import { routing } from '../../i18n/routing'
import '../globals.css'
import { LoadingWindow } from '@/components/Loading/LoadingWindow/LoadingWindow'

export const metadata: Metadata = {}

interface RootLayoutProps {
    children: React.ReactNode,
    params: Promise<{ locale: string }>
}

export default async function RootLayout({
    children,
    params
}: RootLayoutProps) {
    const { locale } = await params
    if (!hasLocale(routing.locales, locale)) {
        notFound()
    }
    let messages
    try {
        messages = (await import(`../../../messages/${locale}.json`)).default
    } catch {
        notFound()
    }

    return (
        <html lang={locale}>
            <head >
                <link rel="icon" href="/favicon/favicon.jpg" />
            </head>
            <body>
                <NextIntlClientProvider locale={locale} messages={messages}>
                    <QueryProvider>
                        <LoadingWindow />
                        {children}
                        <Footer />
                    </QueryProvider>
                </NextIntlClientProvider>
            </body>
        </html>
    )
}

