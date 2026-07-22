
// --- 工具函数 ---

const isPlainObject = v => !!v && 'object' === typeof v && !Array.isArray(v);

const deepStripMeta = value => {
    if (Array.isArray(value)) return value.map(deepStripMeta);
    if (!isPlainObject(value)) return value;

    return Object.fromEntries(
        Object.entries(value)
            .filter(([key]) => !key.startsWith('$'))
            .map(([key, val]) => [key, deepStripMeta(val)])
    );
};

const boolPreprocess = (defaultVal = false) => z.preprocess(v => {
    if ('boolean' === typeof v) return v;
    if ('number' === typeof v) return 0 !== v;
    if ('string' === typeof v) {
        const normalized = v.trim().toLowerCase();
        if (['是', 'true', '1', 'yes', 'y'].includes(normalized)) return true;
        if (['否', 'false', '0', 'no', 'n', ''].includes(normalized)) return false;
    }
    return defaultVal;
}, z.boolean());

const clampNum = (defaultVal, min, max) => z.preprocess(v => {
    if ('number' === typeof v) return v;
    if ('string' === typeof v) {
        const trimmed = v.trim();
        if (!trimmed) return defaultVal;
        const parsed = Number(trimmed);
        return Number.isFinite(parsed) ? parsed : defaultVal;
    }
    return defaultVal;
}, z.number()).prefault(defaultVal).transform(v => _.clamp(v, min, max));

const nonNegativeInt = (defaultVal = 0) => z.preprocess(v => {
    if ('number' === typeof v) return v;
    if ('string' === typeof v) {
        const trimmed = v.trim();
        if (!trimmed) return defaultVal;
        const parsed = Number(trimmed);
        return Number.isFinite(parsed) ? parsed : defaultVal;
    }
    return defaultVal;
}, z.number()).prefault(defaultVal).transform(v => Math.max(0, Math.floor(v)));

const str = (val = '') => z.preprocess(v => 'string' === typeof v ? v : val, z.string()).prefault(val);

const strArray = (val = []) => z.preprocess(v => {
    if (Array.isArray(v)) return v.filter(item => 'string' === typeof item).map(item => item.trim()).filter(Boolean);
    if ('string' === typeof v) {
        const trimmed = v.trim();
        if (!trimmed) return val;
        return trimmed.split(/[、,，;；\n]/).map(item => item.trim()).filter(Boolean);
    }
    return val;
}, z.array(z.string())).prefault(val);

const recordOf = schema => z.preprocess(
    v => isPlainObject(v) ? v : {},
    z.record(z.string(), schema)
).prefault({});

// --- 基础枚举 ---

const weekEnum = z.enum(['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']).prefault('星期一');
const periodEnum = z.enum(['清晨', '上午', '下午', '傍晚', '夜晚', '深夜']).prefault('下午');
const storyModeEnum = z.enum(['日常', '特殊']).prefault('日常');
const storyVolEnum = z.enum(['', 'Vol0', 'Vol1', 'Vol2', 'Vol3', 'Vol4', 'Vol5', 'VolF', 'Vol6', 'VolEX']).prefault('');
const storyChapterEnum = z.enum(['', 'Ch1', 'Ch2', 'Ch3', 'Ch4']).prefault('');

const STORY_CHAPTER_ORDER = ['Ch1', 'Ch2', 'Ch3', 'Ch4'];
const STORY_VOLUME_CHAPTER_COUNTS = {
    Vol0: 1,
    Vol1: 3,
    Vol2: 2,
    Vol3: 4,
    Vol4: 2,
    Vol5: 2,
    VolF: 4,
    Vol6: 3,
    VolEX: 3
};

const storyChapterListSchema = z.preprocess(v => {
    if (Array.isArray(v)) return v;
    if ('string' === typeof v) {
        const trimmed = v.trim();
        if (!trimmed) return [];
        return trimmed.split(/[、,，;；\n]/).map(item => item.trim()).filter(Boolean);
    }
    return [];
}, z.array(storyChapterEnum)).prefault([]);

const normalizeCompletedChapters = (chapters, maxCount) => {
    const allowed = STORY_CHAPTER_ORDER.slice(0, maxCount);
    const unique = _.uniq((Array.isArray(chapters) ? chapters : []).filter(ch => allowed.includes(ch)));
    const normalized = [];

    for (const chapter of allowed) {
        if (!unique.includes(chapter)) break;
        normalized.push(chapter);
    }

    return normalized;
};

// --- 世界信息 ---

const eventSchema = z.object({
    name: str(''),
    type: str(''),
    description: str(''),
    start_date: str(''),
    remaining_duration: str(''),
    end_date: str('')
});

const worldInfoSchema = z.object({
    time: z.object({
        current_date: str(''),
        current_time: str('00:00'),
        day_of_week: weekEnum
    }).prefault({}),
    location: z.object({
        district: str(''),
        detailed_location: str('')
    }).prefault({}),
    environment: z.object({
        weather: str(''),
        period: periodEnum,
        temperature: str('')
    }).prefault({}),
    events: recordOf(eventSchema),
    rumor: str('')
}).prefault({});

// --- 主角 ---

const questRewardSchema = z.object({
    credits: nonNegativeInt(0),
    pyroxene: nonNegativeInt(0)
}).prefault({});

const activeQuestSchema = z.object({
    title: str(''),
    description: str(''),
    complateCondition: str(''),
    progress: clampNum(0, 0, 100),
    rewards: questRewardSchema
});

const completedQuestSchema = z.object({
    title: str('')
});

const protagonistSchema = z.object({
    identity: z.object({
        name: str(''),
        title: str('')
    }).prefault({}),
    currency: z.object({
        credits: nonNegativeInt(0),
        pyroxene: nonNegativeInt(0)
    }).prefault({}),
    quest: z.object({
        active: recordOf(activeQuestSchema),
        complate: recordOf(completedQuestSchema)
    }).prefault({})
}).prefault({});

// --- 主线推进 ---

const storyCompletedSchema = z.object({
    Vol0: storyChapterListSchema,
    Vol1: storyChapterListSchema,
    Vol2: storyChapterListSchema,
    Vol3: storyChapterListSchema,
    Vol4: storyChapterListSchema,
    Vol5: storyChapterListSchema,
    VolF: storyChapterListSchema,
    Vol6: storyChapterListSchema,
    VolEX: storyChapterListSchema
}).prefault({});

const storyCurrentSchema = z.object({
    vol: storyVolEnum,
    chapter: storyChapterEnum,
    seq: nonNegativeInt(0)
}).prefault({});

const storyManagerSchema = z.object({
    enabled: boolPreprocess(true),
    mode: storyModeEnum,
    current: storyCurrentSchema,
    completed_chapters: storyCompletedSchema
}).prefault({}).transform(data => {
    const completed_chapters = {};

    Object.entries(STORY_VOLUME_CHAPTER_COUNTS).forEach(([vol, maxCount]) => {
        completed_chapters[vol] = normalizeCompletedChapters(data.completed_chapters?.[vol], maxCount);
    });

    let mode = '特殊' === data.mode ? '特殊' : '日常';
    let currentVol = data.current?.vol || '';
    let currentChapter = data.current?.chapter || '';
    let currentSeq = Math.max(0, Math.floor(Number(data.current?.seq) || 0));

    if (!STORY_VOLUME_CHAPTER_COUNTS[currentVol]) {
        currentVol = '';
    }

    if (currentVol) {
        const allowed = STORY_CHAPTER_ORDER.slice(0, STORY_VOLUME_CHAPTER_COUNTS[currentVol]);
        if (!allowed.includes(currentChapter)) {
            currentChapter = '';
        }
    }

    if ('日常' === mode) {
        currentVol = '';
        currentChapter = '';
        currentSeq = 0;
    } else {
        if (!currentVol || !currentChapter) {
            mode = '日常';
            currentVol = '';
            currentChapter = '';
            currentSeq = 0;
        } else {
            currentSeq = Math.max(1, currentSeq);
        }
    }

    return {
        ...data,
        mode,
        current: {
            vol: currentVol,
            chapter: currentChapter,
            seq: currentSeq
        },
        completed_chapters
    };
});

// --- 学生关系 ---

const basicInfoSchema = z.object({
    name: str(''),
    school: str(''),
    club: str(''),
    is_in_team: boolPreprocess(false)
}).prefault({});

const appearanceSchema = z.object({
    height: str('160cm'),
    hair_color: str(''),
    hairstyle: str(''),
    eye_color: str(''),
    skin_tone: str('白皙'),
    body_type: str('娇小')
}).prefault({});

const clothingSchema = z.object({
    top: str(''),
    bottom: str(''),
    innerwear: str(''),
    panties: str(''),
    stockings: str(''),
    shoes: str(''),
    accessories: str('')
}).prefault({});

const relationshipSchema = z.object({
    affection: clampNum(0, 0, 100),
    sexual_desire: clampNum(0, 0, 100),
    attitude_towards_sensei: str('尊敬')
}).prefault({});

const mentalStateSchema = z.object({
    current_thoughts: str(''),
    emotional_state: str('平静')
}).prefault({});

const locationInfoSchema = z.object({
    current_location: str(''),
    is_nearby: boolPreprocess(false)
}).prefault({});

const bodyFeaturesSchema = z.object({
    breasts: z.object({
        shape: str('半球形'),
        nipple_color: str('粉色')
    }).prefault({}),
    private_parts: z.object({
        type: str('')
    }).prefault({})
}).prefault({});

const sexualExperienceSchema = z.object({
    virgin: boolPreprocess(true),
    anal_experience: nonNegativeInt(0),
    oral_experience: nonNegativeInt(0),
    sex_count: nonNegativeInt(0),
    partner_count: nonNegativeInt(0),
    first_partner: str(''),
    fetishes: strArray([]),
    important_experiences: strArray([])
}).prefault({}).transform(data => ({
    ...data,
    partner_count: Math.min(data.partner_count, data.sex_count)
}));

const physiologicalStateSchema = z.object({
    vaginal_lubrication: str('正常'),
    nipple_state: str('正常'),
    clitoris_state: str('正常'),
    uterus_state: str('正常'),
    menstrual_cycle: str('正常'),
    pregnancy_state: str('未怀孕')
}).prefault({});

const interactionRecordsSchema = z.object({
    first_meeting: str(''),
    memorable_events: str(''),
    relationship_changes: str(''),
    last_interaction: z.object({
        date: str(''),
        location: str('')
    }).prefault({})
}).prefault({});

const relationshipStudentSchema = z.object({
    basic_info: basicInfoSchema,
    appearance: appearanceSchema,
    clothing: clothingSchema,
    relationship: relationshipSchema,
    mental_state: mentalStateSchema,
    location_info: locationInfoSchema,
    body_features: bodyFeaturesSchema,
    sexual_experience: sexualExperienceSchema,
    physiological_state: physiologicalStateSchema,
    interaction_records: interactionRecordsSchema
}).prefault({});

const systemConfigSchema = z.object({
    对白美化: strArray([])
}).prefault({});

const baseSchema = z.object({
    world_info: worldInfoSchema,
    protagonist: protagonistSchema,
    story_manager: storyManagerSchema,
    relationship_students: recordOf(relationshipStudentSchema),
    系统配置: systemConfigSchema
}).prefault({}).transform(data => {
    Object.values(data.protagonist.quest.active || {}).forEach(quest => {
        if (!quest) return;
        quest.progress = _.clamp(Number(quest.progress) || 0, 0, 100);
        quest.rewards.credits = Math.max(0, Math.floor(Number(quest.rewards?.credits) || 0));
        quest.rewards.pyroxene = Math.max(0, Math.floor(Number(quest.rewards?.pyroxene) || 0));
    });

    Object.values(data.relationship_students || {}).forEach(student => {
        if (!student) return;
        student.relationship.affection = _.clamp(Number(student.relationship.affection) || 0, 0, 100);
        student.relationship.sexual_desire = _.clamp(Number(student.relationship.sexual_desire) || 0, 0, 100);
        student.sexual_experience.sex_count = Math.max(0, Math.floor(Number(student.sexual_experience.sex_count) || 0));
        student.sexual_experience.partner_count = _.clamp(
            Math.floor(Number(student.sexual_experience.partner_count) || 0),
            0,
            student.sexual_experience.sex_count
        );
        student.sexual_experience.anal_experience = Math.max(0, Math.floor(Number(student.sexual_experience.anal_experience) || 0));
        student.sexual_experience.oral_experience = Math.max(0, Math.floor(Number(student.sexual_experience.oral_experience) || 0));
    });

    data.protagonist.currency.credits = Math.max(0, Math.floor(Number(data.protagonist.currency.credits) || 0));
    data.protagonist.currency.pyroxene = Math.max(0, Math.floor(Number(data.protagonist.currency.pyroxene) || 0));

    return data;
});

export const Schema = z.preprocess(deepStripMeta, baseSchema);


export type Schema = z.output<typeof Schema>;
