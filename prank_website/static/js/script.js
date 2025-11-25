// 阻止右键菜单
window.addEventListener('contextmenu', function(e) {
    e.preventDefault();
});

// 阻止F5刷新
window.addEventListener('keydown', function(e) {
    if (e.key === 'F5' || (e.ctrlKey && e.key === 'r') || (e.key === 'F5')) {
        e.preventDefault();
    }
    // 阻止退格键返回上一页
    if (e.key === 'Backspace' && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
        e.preventDefault();
    }
});

// 阻止页面关闭
window.addEventListener('beforeunload', function(e) {
    e.preventDefault();
    e.returnValue = '';
});

// 锁定页面滚动
window.addEventListener('scroll', function() {
    window.scrollTo(0, 0);
});

// 获取按钮元素
const option1 = document.getElementById('option1');
const option2 = document.getElementById('option2');
const questionContainer = document.getElementById('question-container');
const resultContainer = document.getElementById('result-container');

// 选项一：接受选项
option1.addEventListener('click', function() {
    // 隐藏问题容器
    questionContainer.style.display = 'none';
    // 显示结果容器
    resultContainer.style.display = 'block';
    
    // 在静态环境下，本地存储选择结果（不依赖后端）
    try {
        localStorage.setItem('prank_choice', 'option1');
        console.log('选择已保存到本地存储');
    } catch (e) {
        console.log('无法保存选择到本地存储');
    }
    
    // 添加嘲讽动画
    addTauntingEffects();
});

// 选项二：拒绝选项，让按钮移动
option2.addEventListener('mouseover', function() {
    moveButtonAway();
});

option2.addEventListener('click', function(e) {
    e.preventDefault();
    moveButtonAway();
    // 在静态环境下，本地存储选择结果（不依赖后端）
    try {
        localStorage.setItem('prank_choice', 'option2');
        console.log('选择已保存到本地存储');
    } catch (e) {
        console.log('无法保存选择到本地存储');
    }
});

// 让按钮远离鼠标
function moveButtonAway() {
    const windowWidth = window.innerWidth;
    const windowHeight = window.innerHeight;
    const buttonWidth = option2.offsetWidth;
    const buttonHeight = option2.offsetHeight;
    
    // 计算随机位置，但确保按钮在可视区域内
    const maxX = windowWidth - buttonWidth - 50;
    const maxY = windowHeight - buttonHeight - 50;
    
    // 确保新位置离鼠标较远
    let newX, newY;
    do {
        newX = Math.random() * maxX;
        newY = Math.random() * maxY;
    } while (isTooCloseToMouse(newX, newY, buttonWidth, buttonHeight));
    
    // 设置按钮位置
    option2.style.position = 'fixed';
    option2.style.left = newX + 'px';
    option2.style.top = newY + 'px';
    option2.style.zIndex = '9999';
    
    // 添加闪烁效果
    option2.style.animation = 'blink 0.5s infinite';
}

// 检查按钮是否离鼠标太近
function isTooCloseToMouse(buttonX, buttonY, buttonWidth, buttonHeight) {
    // 获取鼠标位置（这里用一个近似值，因为我们没有实时的鼠标位置）
    // 实际上，我们只是让按钮随机移动，足够让用户难以点击
    return false; // 简化版本，让按钮完全随机移动
}

// 添加嘲讽效果
function addTauntingEffects() {
    // 播放声音（如果有）
    // 创建更多嘲讽动画
    const taunts = document.querySelectorAll('.taunt-text');
    taunts.forEach((taunt, index) => {
        taunt.style.animationDelay = (index * 0.3) + 's';
        setTimeout(() => {
            taunt.classList.add('fade-in');
        }, 500 * (index + 1));
    });
    
    // 随机改变文字颜色
    setInterval(() => {
        const colors = ['#ff6b6b', '#ff9f43', '#feca57', '#10ac84', '#ee5a24', '#0abde3'];
        const randomColor = colors[Math.floor(Math.random() * colors.length)];
        taunts.forEach(taunt => {
            taunt.style.color = randomColor;
        });
    }, 500);
    
    // 页面震动
    let shakeInterval = setInterval(() => {
        document.body.style.transform = 'translateX(' + (Math.random() * 10 - 5) + 'px)';
        setTimeout(() => {
            document.body.style.transform = 'translateX(0)';
        }, 50);
    }, 200);
    
    // 5秒后停止震动
    setTimeout(() => {
        clearInterval(shakeInterval);
        document.body.style.transform = 'translateX(0)';
    }, 5000);
    
    // 创建CSS动画效果代替图片
    createAnimationEffect();
}

// 创建动画效果
function createAnimationEffect() {
    const animationDiv = document.createElement('div');
    animationDiv.className = 'taunt-animation';
    
    // 添加到结果容器
    const resultContent = document.querySelector('#result-container .result-content') || resultContainer;
    resultContent.insertBefore(animationDiv, resultContent.firstChild);
}

// 初始页面设置
window.onload = function() {
    window.scrollTo(0, 0);
    // 添加页面加载动画
    questionContainer.style.opacity = '0';
    questionContainer.style.transform = 'scale(0.8)';
    questionContainer.style.transition = 'all 0.5s ease';
    
    setTimeout(() => {
        questionContainer.style.opacity = '1';
        questionContainer.style.transform = 'scale(1)';
    }, 300);
};

// 添加一些额外的恶作剧效果
setTimeout(() => {
    // 偶尔改变选项文字颜色
    setInterval(() => {
        option1.style.backgroundColor = '#4CAF50';
        option2.style.backgroundColor = '#f44336';
        setTimeout(() => {
            option1.style.backgroundColor = '#45a049';
            option2.style.backgroundColor = '#da190b';
        }, 200);
    }, 3000);
}, 5000);