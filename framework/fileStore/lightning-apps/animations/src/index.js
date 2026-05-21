/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2020 RDK Management
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import { Launch } from '@lightningjs/sdk'
import App from './AnimationApp.js'
import ThunderJS from 'ThunderJS'
import { GetURLParameter } from './MediaUtility.js'

function formatURL(input) {
  if (Array.isArray(input)) input = input[0] || ''
  let s = String(input || '').trim()
  if (!s) return ''

  if ((s.startsWith("['") && s.endsWith("']")) || (s.startsWith('["') && s.endsWith('"]'))) {
    s = s.slice(2, -2).trim()
  }

  if ((s.startsWith('"') && s.endsWith('"')) || (s.startsWith("'") && s.endsWith("'"))) {
    s = s.slice(1, -1)
  }

  s = s.replace(/&amp;amp;amp;amp;/g, '&amp;amp;amp;').replace(/&amp;amp;amp;/g, '&amp;amp;')
  return s.trim()
}

(async function getValueFromPersistentStore() {
  try {
    
    if (sessionStorage.getItem('ps_init_done')) return

    const port = Number(GetURLParameter('deviceport')) || 9998
    const thunder = ThunderJS({ host: '127.0.0.1', port })

    const namespace = 'MVS'
    const key = 'lightningURL'
    const res = await thunder.call('org.rdk.PersistentStore', 'getValue', { namespace, key })
    console.log('[GetValuePS] Response from PersistentStore.getValue(): ' + (res ? JSON.stringify(res) : 'null'))

    const value = res?.value || res?.data || res?.result || res?.contents || ''
    const url = formatURL(value)

    if (!/^https?:\/\//i.test(url)) {
      console.log('[GetValuePS] Invalid http(s) URL is obtained from PersistentStore')
      return
    }

    const current = window.location.href
    if (current === url) {
      console.log('[GetValuePS] The current lightning animation URL matches the URL obtained from PersistentStore')
      return
    }

    console.log('[GetValuePS] Loading the formatted lightning animation URL fetched from PersistentStore: ' + url)
    sessionStorage.setItem('ps_init_done', '1')
    window.location.replace(url)

  } catch (e) {
    console.log('[GetValuePS] Error occurred in getValueFromPersistentStore: ' + (e && (e.message || JSON.stringify(e))))
  }
})()

export default function() {
  return Launch(App, ...arguments)
}
