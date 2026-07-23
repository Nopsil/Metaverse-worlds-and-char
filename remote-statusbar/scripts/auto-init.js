$(async function initMvuDefaults () {
  await waitGlobalInitialized('Mvu');

  const DEFAULTS = {
    stat_data: {
      selected_character: '',
      selected_scenario: 0,
      phase: 'lobby',
      present_characters: '',
      characters: {
        airine: { name: 'airine', affection: 0, relationship: '', mood: '', clothing: '', inner_thought: '', body_state: '正常', clothing_integrity: '整齐', pose: '站立' },
        bathsheba: { name: 'bathsheba', affection: 0, relationship: '', mood: '', clothing: '', inner_thought: '', body_state: '正常', clothing_integrity: '整齐', pose: '站立' },
        lena: { name: 'lena', affection: 0, relationship: '', mood: '', clothing: '', inner_thought: '', body_state: '正常', clothing_integrity: '整齐', pose: '站立' },
        meme: { name: 'meme', affection: 0, relationship: '', mood: '', clothing: '', inner_thought: '', body_state: '正常', clothing_integrity: '整齐', pose: '站立' },
        belzeebul: { name: 'belzeebul', affection: 0, relationship: '', mood: '', clothing: '', inner_thought: '', body_state: '正常', clothing_integrity: '整齐', pose: '站立' }
      }
    }
  };

  function writeDefaults(source) {
    try {
      var msgId = getCurrentMessageId();
      var current = Mvu.getMvuData({ type: 'message', message_id: msgId });
      if (current && current.stat_data && current.stat_data.selected_character) return; /* already set */
      Mvu.replaceMvuData(DEFAULTS, { type: 'message', message_id: msgId });
    } catch (e) {}
  }

  /* On variable init (Swipe select / first process) */
  eventOn(Mvu.events.VARIABLE_INITIALIZED, function() { setTimeout(writeDefaults, 200); });

  /* Also try on first message receive (fallback for lobby flow) */
  eventOn('MESSAGE_RECEIVED', function() { setTimeout(writeDefaults, 500); });
});
