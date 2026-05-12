const fs = require("fs");
const path = require("path");

/**
 * 配置区域
 */
const CONFIG = {
    // 源音频目录
    inputDir: path.join(__dirname, "output", "slicer_opt"),
    // 输出 list 文件目录
    outputDir: path.join(__dirname, "output", "asr_opt"),
    // 默认角色名
    defaultSpeaker: "iris_",
    // 强制转换为大写的语种标签映射
    langMapping: {
        zh: "ZH",
        en: "EN",
        ja: "JA",
        ko: "KO",
    },
};

const outputFile = path.join(CONFIG.outputDir, "slicer_opt.list");

function generateSlicerList() {
    try {
        // 1. 检查并创建输出目录
        if (!fs.existsSync(CONFIG.outputDir)) {
            fs.mkdirSync(CONFIG.outputDir, { recursive: true });
        }

        // 2. 读取源目录下的所有文件
        if (!fs.existsSync(CONFIG.inputDir)) {
            console.error(`错误: 找不到输入目录 ${CONFIG.inputDir}`);
            return;
        }

        const files = fs.readdirSync(CONFIG.inputDir);

        // 3. 过滤 wav 并解析格式
        const listContent = files
            .filter((file) => path.extname(file).toLowerCase() === ".wav")
            .map((file) => {
                // 分解 "语种_文件名.wav"
                const firstUnderscore = file.indexOf("_");

                if (firstUnderscore === -1) {
                    console.warn(`警告: 文件名格式不符，已跳过 -> ${file}`);
                    return null;
                }

                const rawLang = file
                    .substring(0, firstUnderscore)
                    .toLowerCase();
                const lang =
                    CONFIG.langMapping[rawLang] || rawLang.toUpperCase();

                // 获取音频文件的绝对路径（训练脚本通常需要绝对路径）
                const absolutePath = path.resolve(CONFIG.inputDir, file);

                // GPT-SoVITS List 格式: 路径|角色名|语种|内容(留空等ASR)
                return `${absolutePath}|${CONFIG.defaultSpeaker}|${lang}|`;
            })
            .filter((line) => line !== null);

        // 4. 写入文件
        fs.writeFileSync(outputFile, listContent.join("\n"), "utf8");

        console.log("------------------------------------------");
        console.log(`生成成功！`);
        console.log(`文件位置: ${outputFile}`);
        console.log(`处理条数: ${listContent.length}`);
        console.log("------------------------------------------");
    } catch (err) {
        console.error("脚本运行出错:", err.message);
    }
}

generateSlicerList();
