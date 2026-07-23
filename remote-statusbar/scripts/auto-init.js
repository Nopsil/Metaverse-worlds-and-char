let initialized = false;

function initIfEmpty() {
  if (initialized) return;
  try {
    const all = getAllVariables();
    const sc = all?.stat_data?.selected_character;
    if (!sc) return; // wait for character selection
    const chars = all?.stat_data?.characters || {};
    if (chars[sc]?.affection == null || chars[sc]?.affection === 0) {
      // Variables not yet set by AI - initialize now
      const data = {
        stat_data: {
          selected_character: sc,
          selected_scenario: all.stat_data.selected_scenario || 0,
          phase: 'playing',
          characters: {
            [sc]: {
              name: sc,
              affection: 0,
              relationship: '陌生人',
              mood: '',
              clothing: '',
              inner_thought: '',
              body_state: '正常',
              clothing_integrity: '整齐',
              pose: '站立'
            }
          }
        }
      };
      insertOrAssignVariables(data, { type: 'chat' });
      initialized = true;
    }
  } catch (e) {}
}

$(async () => {
  await waitGlobalInitialized('Mvu');
  eventOn('MESSAGE_RECEIVED', () => setTimeout(initIfEmpty, 500));
  eventOn('MESSAGE_UPDATED', () => setTimeout(initIfEmpty, 500));
  initIfEmpty();
});
