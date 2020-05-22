import React from 'react';
import Link from 'next/link'

import utilStyles from '../styles/utils.module.css'

export default function Links( { links } ) {

    return (
        <ul className={utilStyles.list}>
            {links.map(({ id, text }) => (
                <li className={utilStyles.listItem} key={id}>
                    <Link href="/texts/[id]" as={`/texts/${id}`}>
                        <a>{text}</a>
                    </Link>
                </li>
            ))}
        </ul>
    );
}

