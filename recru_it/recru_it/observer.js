/* Read-only observations. No request headers, bodies, or click behavior are changed. */
(() => {
  if (window.__recruObserver) return;
  const DETAIL = '/web/Jobinfo/getBoardJobDetail';
  const LIST = '/web/Jobinfo/getJobBoardList';
  const selectors = {
    title: '#detail_info div.ft5.NotoSansM',
    site: 'div.time.ft11.col_gra04.NotoSansL',
    type: '#detail_info div.ft11 div.ft10',
    pay: '#detail_info div.col_blu02.ft10 > div',
    etcs: '#detail_info div.ft11.col_blu02',
    people: "#detail_info div.ft11 div.ft10[style='display: flex;']",
    phone: '#detail_info div.ft11 div.ft10.RobotoM',
    detail: '#detail_info p.ft10.lin_h2',
    imageURL: '#detail_info > div > div > div > div > img'
  };
  const multi = new Set(['etcs', 'people']);
  const requests = [];
  let attempt = null, sequence = 0, diagnosticErrors = 0, cachedVue = null;
  let listVm = null, listEvents = 0, listComplete = false;
  let movement = null;
  function movementSample() {
    if (!movement) throw Error('movement_observer_unavailable');
    const m = movement, now = performance.now(), card = m.card;
    let reason = 'detached', geometry = [], point = null;
    if (card.isConnected && card.getClientRects().length) {
      const r = card.getClientRects()[0];
      geometry = [r.x, r.y, r.width, r.height];
      for (let parent = card.parentElement; parent; parent = parent.parentElement) {
        geometry.push(parent.scrollLeft, parent.scrollTop);
      }
      geometry.push(window.scrollX, window.scrollY);
      // Match WebDriver's in-view center, including viewport clipping. The
      // hit test also catches clipping/covering by a nested scrolling container.
      const left = Math.max(0, Math.min(r.x, r.x + r.width));
      const right = Math.min(innerWidth, Math.max(r.x, r.x + r.width));
      const top = Math.max(0, Math.min(r.y, r.y + r.height));
      const bottom = Math.min(innerHeight, Math.max(r.y, r.y + r.height));
      reason = 'outside_view';
      if (right > left && bottom > top) {
        point = [Math.floor((left + right) / 2), Math.floor((top + bottom) / 2)];
        const hit = document.elementFromPoint(...point);
        reason = card.matches(':disabled') ? 'disabled' :
          hit && (hit === card || card.contains(hit)) ? 'ready' : 'obstructed';
      }
    }
    const changed = !m.geometry || geometry.length !== m.geometry.length ||
      geometry.some((value, i) => Math.abs(value - m.geometry[i]) > 0.01);
    if (changed) m.changes++;
    // A paused observer cannot establish continuous stability. Compare against
    // a stable anchor, so tiny movements cannot accumulate unnoticed.
    if (changed || reason !== 'ready' || m.reason !== 'ready' || now - m.sampled > 100) {
      m.since = now;
      m.geometry = geometry;
    }
    if (reason === 'obstructed') m.obstructed++;
    m.reason = reason;
    m.sampled = now;
    m.state = {ok: reason === 'ready' && now - m.since >= m.stableMs,
      reason: reason === 'ready' && now - m.since < m.stableMs ? 'moving' : reason,
      stable_seconds: (now - m.since) / 1000, elapsed_seconds: (now - m.started) / 1000,
      position_changes: m.changes, obstructed_samples: m.obstructed, point};
    return m.state;
  }
  function stopMovement(number) {
    if (movement && (number === undefined || movement.number === number)) {
      cancelAnimationFrame(movement.frame);
      movement = null;
    }
  }
  const vue = () => {
    const list = document.querySelector('.scrollsection');
    if (cachedVue && !cachedVue._isDestroyed && cachedVue.$el.contains(list)) return cachedVue;
    const seen = new Set();
    const find = vm => {
      if (!vm || seen.has(vm)) return null;
      seen.add(vm);
      if ('recuitDetail' in vm && vm.$el.contains(list)) return vm;
      for (const child of vm.$children || []) { const found = find(child); if (found) return found; }
      return null;
    };
    // A wrapper component can replace $el.__vue__ after scrolling; search the
    // owning component tree as well as the DOM ancestors.
    for (let el = list; el; el = el.parentElement) {
      const found = find(el.__vue__);
      if (found) { cachedVue = found; return found; }
    }
    throw Error('detail_model_unavailable');
  };
  const text = value => String(value == null ? '' : value);
  // Only identifiers and numeric result codes leave the page. Never retain a
  // response body, error message, user/account ID, or arbitrary string value.
  const jobId = value => {
    if (typeof value === 'number' && Number.isSafeInteger(value) && value >= 0) return String(value);
    return typeof value === 'string' && /^\d{1,20}$/.test(value) ? value : null;
  };
  function responseDiagnostic(xhr) {
    try {
      let body;
      if (xhr.responseType === 'json') body = xhr.response;
      else if (!xhr.responseType || xhr.responseType === 'text') {
        const source = xhr.responseText;
        if (typeof source !== 'string') return {state: 'unavailable'};
        if (!source.length) return {state: 'empty'};
        if (source.length > 262144) return {state: 'too_large'};
        try { body = JSON.parse(source); } catch (_) { return {state: 'invalid_json'}; }
      } else return {state: 'unsupported_type'};
      if (!body || typeof body !== 'object' || Array.isArray(body)) return {state: 'not_object'};
      const own = key => Object.prototype.hasOwnProperty.call(body, key);
      const value = body.rescode;
      const code = typeof value === 'number' ? value :
        typeof value === 'string' && /^-?\d{1,4}$/.test(value) ? Number(value) : null;
      const validCode = Number.isInteger(code) && Math.abs(code) <= 9999;
      const data = body.data;
      const dataState = !own('data') ? 'missing' : data === null ? 'null' : Array.isArray(data) ?
        (data.length ? 'array' : 'empty_array') : typeof data === 'object' ?
        (Object.keys(data).length ? 'object' : 'empty_object') :
        data === '' ? 'empty_string' : typeof data;
      return {state: 'captured', rescode: validCode ? code : null,
        rescode_state: !own('rescode') ? 'missing' : validCode ? 'numeric' : 'unsupported',
        data_state: dataState, job_id: data && typeof data === 'object' && !Array.isArray(data) ? jobId(data.idx) : null};
    } catch (_) {
      // A missing diagnostic cannot make a snapshot valid or interrupt the app.
      return {state: 'unavailable'};
    }
  }
  function identityDiagnostic(current) {
    try {
      const model = vue().recuitDetail;
      return {state: !model ? 'missing' : model === current.previous ? 'unchanged' :
        text(model.idx) !== current.id ? 'different_id' : 'matches',
        model_present: Boolean(model), model_replaced: Boolean(model) && model !== current.previous,
        model_job_id: model ? jobId(model.idx) : null};
    } catch (_) { return {state: 'unavailable'}; }
  }
  const canonical = value => text(value).replace(/[\u200b\u200e\u200f]/g, '').replace(/\s+/g, ' ').trim();
  const trim = value => value.replace(/^[^\S\u00a0]+|[^\S\u00a0]+$/g, '');
  const rendered = root => {
    // Match WebDriver's block/text-node whitespace rules for this site's simple
    // DOM. In particular, a newline INSIDE one text node is not a block boundary.
    // Reference: Selenium javascript/atoms/dom.js getVisibleText (Apache-2.0).
    // Every saved value is also checked against the installed driver's .text.
    const lines = [''];
    const inline = new Set(['inline', 'inline-block', 'inline-table', 'none', 'table-cell', 'table-column', 'table-column-group']);
    const last = () => lines[lines.length - 1];
    const nonempty = () => /\S/.test(last());
    const visit = el => {
      const style = getComputedStyle(el);
      if (style.display === 'none') return;
      if (el.tagName === 'BR') { lines.push(''); return; }
      const cell = el.tagName === 'TD' || style.display === 'table-cell';
      const block = !cell && !inline.has(style.display);
      const previous = el.previousElementSibling;
      const followsRunIn = previous && getComputedStyle(previous).display === 'run-in' && style.cssFloat === 'none';
      if (block && !followsRunIn && nonempty()) lines.push('');
      const shown = window.__recruDisplayed(el, false);
      for (const node of el.childNodes) {
        if (node.nodeType === Node.ELEMENT_NODE) { visit(node); continue; }
        if (node.nodeType !== Node.TEXT_NODE || !shown) continue;
        let value = node.nodeValue.replace(/[\u200b\u200e\u200f]/g, '').replace(/\r\n|\r/g, '\n');
        if (['normal', 'nowrap'].includes(style.whiteSpace)) value = value.replaceAll('\n', ' ');
        value = ['pre', 'pre-wrap'].includes(style.whiteSpace)
          ? value.replace(/[ \f\t\v\u2028\u2029]/g, '\u00a0')
          : value.replace(/[ \f\t\v\u2028\u2029]+/g, ' ');
        if (style.textTransform === 'uppercase') value = value.toUpperCase();
        else if (style.textTransform === 'lowercase') value = value.toLowerCase();
        else if (style.textTransform !== 'none') throw Error('unsupported_text_transform');
        if (last().endsWith(' ') && value.startsWith(' ')) value = value.slice(1);
        lines[lines.length - 1] += value;
      }
      if (cell && last() && !last().endsWith(' ')) lines[lines.length - 1] += ' ';
      if (block && style.display !== 'run-in' && nonempty()) lines.push('');
    };
    visit(root);
    return trim(lines.map(trim).join('\n')).replace(/\u00a0/g, ' ');
  };
  const equal = (a, b) => JSON.stringify(a) === JSON.stringify(b);
  const urlKey = value => {
    const url = new URL(value, document.baseURI);
    // Decode path segments individually: encoded slashes must not change identity.
    return JSON.stringify([url.origin, url.pathname.split('/').map(decodeURIComponent), url.search, url.hash]);
  };
  const cards = () => {
    const vm = vue(), nodes = [...document.querySelectorAll('div.scrollsection > div.box.pointer')];
    const nodeSet = new Set(nodes), records = new Map();
    // Resolve each card through its Vue render key, not a positional zip of columns.
    const visit = vnode => {
      if (!vnode) return;
      const match = /^(normalRecruList|emergenRecruList)(\d+)$/.exec(text(vnode.key));
      const emergency = Number.isInteger(vnode.key) && vnode.key >= 0;
      if ((match || emergency) && nodeSet.has(vnode.elm)) {
        if (records.has(vnode.elm)) throw Error('duplicate_card_identity');
        records.set(vnode.elm, match ? vm[match[1]][Number(match[2])] : vm.emergenRecruList[vnode.key]);
      }
      (vnode.children || []).forEach(visit);
    };
    visit(vm._vnode);
    return nodes.map(node => {
      const record = records.get(node);
      if (!record || !record.idx) throw Error('card_identity_unavailable');
      return {node, record};
    });
  };
  function snapshot() {
    if (!attempt || attempt.clicked === null) return {ok: false, reason: 'click_not_observed'};
    const own = requests.filter(r => r.attempt === attempt.number && r.kind === 'detail');
    if (own.some(r => [429, 503].includes(r.status))) return {ok: false, reason: 'source_unavailable'};
    const vm = vue(), model = vm.recuitDetail;
    if (!model || model === attempt.previous || text(model.idx) !== attempt.id) return {ok: false, reason: 'identity'};
    // An unfinished earlier request could overwrite the same ID during a retry.
    if (requests.some(r => r.kind === 'detail' && !r.done)) return {ok: false, reason: 'request_pending'};
    if (own.length !== 1 || own[0].status !== 200) return {ok: false, reason: 'request_evidence'};
    const raw = {}, semantic = {};
    for (const [key, selector] of Object.entries(selectors)) {
      const elements = [...document.querySelectorAll(selector)];
      if (key === 'imageURL') {
        if (elements.length > 1) return {ok: false, reason: 'image_count'};
        raw[key] = elements.length ? elements[0].src : '';
      } else if (multi.has(key)) {
        raw[key] = elements.map(rendered);
        semantic[key] = elements.map(el => canonical(el.textContent));
      } else {
        if (!elements.length) return {ok: false, reason: 'missing_' + key};
        raw[key] = rendered(elements[0]);
        semantic[key] = canonical(elements[0].textContent);
      }
    }
    const labels = {1: '일급', 2: '주급', 3: '월급'};
    const expected = {
      title: canonical(model.title),
      site: canonical('location_on ' + text(model.locNm) + ' ' + text(model.locDetailNm)),
      type: canonical(text(model.cateNm).replaceAll(',', ', ')),
      pay: canonical(labels[model.priceDiv] ? labels[model.priceDiv] + text(model.pricepub) : '협의 후 결정'),
      phone: canonical(model.phone), detail: canonical(model.content),
      etcs: [model.sex === 'M' ? '남성' : model.sex === 'F' ? '여성' : '성별 무관'],
      people: []
    };
    for (const values of [model.completlist, model.workcatelist]) {
      if (values) values.forEach((value, index) => expected.etcs.push(canonical(value + (index < values.length - 1 ? ',' : ''))));
    }
    let gongs = [];
    if (model.workDiv === '99') gongs = model.gongDiv;
    else if (model.gongDiv === '99') gongs = model.workDiv;
    if (!Array.isArray(gongs)) return {ok: false, reason: 'people_model'};
    gongs.forEach((gong, index) => expected.people.push(canonical(
      (['초보', '조공', '준공', '기공'][gong] || '') +
      (model.workDiv === '99' ? ' ' : '') + text(model.workNum[gong]) + '명' + (index < gongs.length - 1 ? ' / ' : '')
    )));
    expected.people.push(canonical(model.manager));
    const mismatches = Object.keys(expected).filter(key => !equal(semantic[key], expected[key]));
    const expectedImage = vm.$global.isEmpty(model.recuritImg) ? '' : vm.$config.getS3Prefix() + '/' + model.recuritImg;
    if ((!expectedImage !== !raw.imageURL) || (expectedImage && urlKey(expectedImage) !== urlKey(raw.imageURL))) mismatches.push('imageURL');
    if (mismatches.length) return {ok: false, reason: 'fields', mismatches};
    return {ok: true, raw, attempt: attempt.number, requestSequence: own[0].sequence};
  }
  function observeReady() {
    if (!attempt || attempt.clicked === null || attempt.ready !== null) return;
    try {
      if (snapshot().ok) attempt.ready = performance.now();
    } catch (_) { diagnosticErrors++; }
  }
  const open = XMLHttpRequest.prototype.open, send = XMLHttpRequest.prototype.send;
  const info = new WeakMap();
  XMLHttpRequest.prototype.open = function(method, url, ...args) {
    info.set(this, {method, path: new URL(url, document.baseURI).pathname});
    return open.call(this, method, url, ...args);
  };
  XMLHttpRequest.prototype.send = function(...args) {
    const metadata = info.get(this), xhr = this;
    if (!metadata || ![DETAIL, LIST].includes(metadata.path)) return send.apply(this, args);
    let id = '';
    try { id = text(JSON.parse(args[0]).idx); } catch (_) { /* List requests do not need an ID. */ }
    const record = {sequence: ++sequence, kind: metadata.path === DETAIL ? 'detail' : 'list',
      attempt: attempt && attempt.clicked !== null && id === attempt.id ? attempt.number : null,
      started: performance.now(), done: false, status: null};
    if (record.kind === 'detail') record.job_id = jobId(id);
    requests.push(record);
    xhr.addEventListener('loadend', () => {
      record.done = true; record.status = xhr.status; record.finished = performance.now();
      if (record.kind === 'detail') record.response_diagnostic = responseDiagnostic(xhr);
      observeReady();
    }, {once: true});
    // The name appears in CDP's initiator stack, linking a request without adding
    // headers or comparing the browser clock with CDP's monotonic clock.
    const name = 'recru_request_' + record.sequence;
    const call = {[name]() { return send.apply(xhr, args); }};
    return call[name]();
  };
  document.addEventListener('click', event => {
    if (attempt && attempt.card.contains(event.target) && attempt.clicked === null) {
      attempt.clicked = performance.now();
    }
  }, true);
  new MutationObserver(observeReady).observe(document, {subtree: true, childList: true, characterData: true, attributes: true});
  window.__recruObserver = {
    selectors,
    beginMovement(card, number, stableSeconds) {
      stopMovement();
      const now = performance.now();
      movement = {card, number, stableMs: stableSeconds * 1000, started: now,
        sampled: now, since: now, geometry: null, changes: 0, obstructed: 0};
      const tick = () => {
        if (!movement || movement.number !== number) return;
        movementSample();
        movement.frame = requestAnimationFrame(tick);
      };
      tick();
    },
    movementStatus(number) {
      if (!movement || movement.number !== number) throw Error('movement_attempt_mismatch');
      return movementSample();
    },
    stopMovement,
    listState() {
      const vm = vue();
      if (listVm !== vm) {
        if (!vm.$events || typeof vm.$events.$on !== 'function') throw Error('list_events_unavailable');
        listVm = vm; listEvents = 0; listComplete = false;
        vm.$events.$on('recuit_pageload', value => {
          listEvents++;
          listComplete = value === 'complete';
        });
      }
      const listRequests = requests.filter(r => r.kind === 'list');
      const networkPending = listRequests.filter(r => !r.done).length;
      return {count: document.querySelectorAll('div.scrollsection > div.box.pointer').length,
        modelCount: vm.normalRecruList.length + vm.emergenRecruList.length,
        pending: networkPending > 0 || vm.loadFlag === true,
        networkPending, loadFlag: vm.loadFlag === true, requestsStarted: listRequests.length,
        events: listEvents, complete: listComplete};
    },
    salaryCard(card) {
      const match = cards().find(entry => entry.node === card);
      if (!match) throw Error('card_identity_unavailable');
      const pay = card.querySelector('div.sub_info.foot > div > div');
      return {priceDiv: text(match.record.priceDiv), price: text(match.record.price),
        pay: pay ? rendered(pay) : ''};
    },
    unavailable() { return requests.some(r => [429, 503].includes(r.status)); },
    health() {
      try {
        vue();
        return {available: true, pendingDetail: requests.some(r => r.kind === 'detail' && !r.done)};
      } catch (_) { return {available: false}; }
    },
    arm(card, number) {
      if (requests.some(r => r.kind === 'detail' && !r.done)) throw Error('previous_detail_pending');
      const match = cards().find(entry => entry.node === card);
      if (!match) throw Error('card_identity_unavailable');
      attempt = {number, id: text(match.record.idx), card, previous: vue().recuitDetail, clicked: null, ready: null};
      return true;
    },
    snapshot,
    summary(number = attempt && attempt.number) {
      // Return only this attempt. The complete history stays in the page for
      // pending-request/status checks, not in every WebDriver response.
      return {diagnosticErrors, requests: requests.filter(r => r.attempt === number).map(r => ({...r})),
        attempt: attempt ? {number: attempt.number, clicked: attempt.clicked, ready: attempt.ready,
          readySeconds: attempt.ready === null ? null : (attempt.ready - attempt.clicked) / 1000,
          job_id: jobId(attempt.id), identity: attempt.number === number ? identityDiagnostic(attempt) : null} : null};
    },
    overview() {
      return {userAgent: navigator.userAgent, cards: cards().map(({node, record}) => ({
        simple: rendered(node.querySelector('div.scrap_wrap.ft12.col_ora01')).split('\n')[0],
        site: rendered(node.querySelector('div.sub_info.foot div.ft12')).replaceAll('\n', '').replace('location_on', ''),
        pay: rendered(node.querySelector('div.sub_info.foot > div > div')),
        priceDiv: text(record.priceDiv)
      }))};
    }
  };
})();
