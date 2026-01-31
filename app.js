// ===== Global State =====
let incomeCategories = [];
let expenseCategories = [];
let expenseChart = null;
let incomeExpenseChart = null;

// ===== Initialize App =====
document.addEventListener('DOMContentLoaded', () => {
    initializeDateInputs();
    initializeMonthSelector();
    loadCategories();
    loadTransactions();
    loadAnalysis();
    setupEventListeners();
});

// ===== Initialize Month Selector =====
function initializeMonthSelector() {
    const today = new Date();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const year = today.getFullYear();
    document.getElementById('monthSelector').value = `${year}-${month}`;
}

// ===== Set Default Dates =====
function initializeDateInputs() {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('incomeDate').value = today;
    document.getElementById('expenseDate').value = today;
}

// ===== Load Categories =====
async function loadCategories() {
    try {
        const response = await fetch('/api/categories');
        const data = await response.json();

        incomeCategories = data.income_categories;
        expenseCategories = data.expense_categories;

        populateCategories();
    } catch (error) {
        console.error('Error loading categories:', error);
        showToast('Error loading categories', 'error');
    }
}

function populateCategories() {
    const incomeSelect = document.getElementById('incomeCategory');
    const expenseSelect = document.getElementById('expenseCategory');

    // Populate income categories
    incomeCategories.forEach(category => {
        const option = document.createElement('option');
        option.value = category;
        option.textContent = category;
        incomeSelect.appendChild(option);
    });

    // Populate expense categories
    expenseCategories.forEach(category => {
        const option = document.createElement('option');
        option.value = category;
        option.textContent = category;
        expenseSelect.appendChild(option);
    });
}

// ===== Event Listeners =====
function setupEventListeners() {
    // Income form submission
    document.getElementById('incomeForm').addEventListener('submit', handleIncomeSubmit);

    // Expense form submission
    document.getElementById('expenseForm').addEventListener('submit', handleExpenseSubmit);

    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', handleTabSwitch);
    });

    // Month Selector change
    document.getElementById('monthSelector').addEventListener('change', () => {
        loadTransactions();
        loadAnalysis();
    });
}

// ===== Handle Income Submission =====
async function handleIncomeSubmit(e) {
    e.preventDefault();

    const formData = {
        amount: parseFloat(document.getElementById('incomeAmount').value),
        category: document.getElementById('incomeCategory').value,
        source: document.getElementById('incomeSource').value,
        date: document.getElementById('incomeDate').value,
        description: document.getElementById('incomeDescription').value
    };

    try {
        const response = await fetch('/api/income', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (data.success) {
            showToast('Income added successfully!', 'success');
            e.target.reset();
            initializeDateInputs();
            loadTransactions();
            loadAnalysis();
        } else {
            showToast(data.message, 'error');
        }
    } catch (error) {
        console.error('Error adding income:', error);
        showToast('Error adding income', 'error');
    }
}

// ===== Handle Expense Submission =====
async function handleExpenseSubmit(e) {
    e.preventDefault();

    const formData = {
        amount: parseFloat(document.getElementById('expenseAmount').value),
        category: document.getElementById('expenseCategory').value,
        date: document.getElementById('expenseDate').value,
        description: document.getElementById('expenseDescription').value
    };

    try {
        const response = await fetch('/api/expense', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (data.success) {
            showToast('Expense added successfully!', 'success');
            e.target.reset();
            initializeDateInputs();
            loadTransactions();
            loadAnalysis();
        } else {
            showToast(data.message, 'error');
        }
    } catch (error) {
        console.error('Error adding expense:', error);
        showToast('Error adding expense', 'error');
    }
}

// ===== Load Transactions =====
async function loadTransactions() {
    try {
        const monthValue = document.getElementById('monthSelector').value; // YYYY-MM
        let queryParams = '';

        if (monthValue) {
            const [year, month] = monthValue.split('-');
            queryParams = `?year=${year}&month=${month}`;
        }

        const response = await fetch(`/api/transactions${queryParams}`);
        const data = await response.json();

        if (data.success) {
            displayIncomes(data.incomes);
            displayExpenses(data.expenses);
        }
    } catch (error) {
        console.error('Error loading transactions:', error);
    }
}

function displayIncomes(incomes) {
    const tbody = document.getElementById('incomesTableBody');

    if (incomes.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="no-data">No income recorded yet</td></tr>';
        return;
    }

    tbody.innerHTML = incomes.map(income => `
        <tr>
            <td>${formatDate(income.date)}</td>
            <td>${income.category}</td>
            <td>${income.source || '-'}</td>
            <td style="font-weight: 600; color: #10b981;">${formatCurrency(income.amount)}</td>
            <td>
                <button class="btn btn-danger" onclick="deleteIncome(${income.id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

function displayExpenses(expenses) {
    const tbody = document.getElementById('expensesTableBody');

    if (expenses.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="no-data">No expenses recorded yet</td></tr>';
        return;
    }

    tbody.innerHTML = expenses.map(expense => `
        <tr>
            <td>${formatDate(expense.date)}</td>
            <td>${expense.category}</td>
            <td>${formatCurrency(expense.amount)}</td>
            <td>${expense.description || '-'}</td>
            <td>
                <button class="btn btn-danger" onclick="deleteExpense(${expense.id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

// ===== Delete Functions =====
async function deleteIncome(id) {
    if (!confirm('Are you sure you want to delete this income record?')) return;

    try {
        const response = await fetch(`/api/income/${id}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
            showToast('Income deleted successfully', 'success');
            loadTransactions();
            loadAnalysis();
        } else {
            showToast(data.message, 'error');
        }
    } catch (error) {
        console.error('Error deleting income:', error);
        showToast('Error deleting income', 'error');
    }
}

async function deleteExpense(id) {
    if (!confirm('Are you sure you want to delete this expense record?')) return;

    try {
        const response = await fetch(`/api/expense/${id}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
            showToast('Expense deleted successfully', 'success');
            loadTransactions();
            loadAnalysis();
        } else {
            showToast(data.message, 'error');
        }
    } catch (error) {
        console.error('Error deleting expense:', error);
        showToast('Error deleting expense', 'error');
    }
}

// ===== Load Analysis =====
async function loadAnalysis() {
    try {
        const monthValue = document.getElementById('monthSelector').value; // YYYY-MM
        let queryParams = '';

        if (monthValue) {
            const [year, month] = monthValue.split('-');
            queryParams = `?year=${year}&month=${month}`;
        }

        const response = await fetch(`/api/analysis${queryParams}`);
        const data = await response.json();

        if (data.success) {
            const analysis = data.analysis;
            updateClassification(analysis.classification);
            updateMetrics(analysis.metrics);
            updateInsights(analysis.insights);
            updateCharts(analysis);
        }
    } catch (error) {
        console.error('Error loading analysis:', error);
    }
}

function updateClassification(classification) {
    document.getElementById('classificationEmoji').textContent = classification.emoji;
    document.getElementById('classificationLabel').textContent = classification.label;
    document.getElementById('classificationLabel').style.color = classification.color;
    document.getElementById('classificationDescription').textContent = classification.description;
}

function updateMetrics(metrics) {
    document.getElementById('totalIncome').textContent = formatCurrency(metrics.total_income);
    document.getElementById('totalExpenses').textContent = formatCurrency(metrics.total_expenses);
    document.getElementById('totalSavings').textContent = formatCurrency(metrics.total_savings);
    document.getElementById('savingsRate').textContent = metrics.savings_rate.toFixed(1) + '%';

    // Color code savings
    const savingsElement = document.getElementById('totalSavings');
    if (metrics.total_savings > 0) {
        savingsElement.style.color = '#10b981';
    } else if (metrics.total_savings < 0) {
        savingsElement.style.color = '#ef4444';
    }
}

function updateInsights(insights) {
    const insightsList = document.getElementById('insightsList');
    const recommendationsList = document.getElementById('recommendationsList');

    // Update insights
    if (insights.insights.length > 0) {
        insightsList.innerHTML = insights.insights.map(insight =>
            `<li>${insight}</li>`
        ).join('');
    }

    // Update recommendations
    if (insights.recommendations.length > 0) {
        recommendationsList.innerHTML = insights.recommendations.map(rec =>
            `<li>${rec}</li>`
        ).join('');
    }
}

function updateCharts(analysis) {
    updateExpenseBreakdownChart(analysis.category_breakdown);
    updateIncomeExpenseChart(analysis.metrics);
}

// ===== Expense Breakdown Chart =====
function updateExpenseBreakdownChart(categoryBreakdown) {
    const ctx = document.getElementById('expenseBreakdownChart').getContext('2d');

    if (expenseChart) {
        expenseChart.destroy();
    }

    const categories = categoryBreakdown.categories;

    if (categories.length === 0) {
        // Show "No data" message
        ctx.font = '16px Inter';
        ctx.fillStyle = '#6b6b8f';
        ctx.textAlign = 'center';
        ctx.fillText('No expense data available', ctx.canvas.width / 2, ctx.canvas.height / 2);
        return;
    }

    const labels = categories.map(c => c.category);
    const data = categories.map(c => c.amount);
    const colors = generateColors(categories.length);

    expenseChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors,
                borderColor: '#1a1a2e',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#a0a0c0',
                        padding: 15,
                        font: {
                            size: 12,
                            family: 'Inter'
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const label = context.label || '';
                            const value = formatCurrency(context.parsed);
                            const percentage = categories[context.dataIndex].percentage.toFixed(1);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// ===== Income vs Expense Chart =====
function updateIncomeExpenseChart(metrics) {
    const ctx = document.getElementById('incomeVsExpenseChart').getContext('2d');

    if (incomeExpenseChart) {
        incomeExpenseChart.destroy();
    }

    if (metrics.total_income === 0 && metrics.total_expenses === 0) {
        ctx.font = '16px Inter';
        ctx.fillStyle = '#6b6b8f';
        ctx.textAlign = 'center';
        ctx.fillText('No data available', ctx.canvas.width / 2, ctx.canvas.height / 2);
        return;
    }

    incomeExpenseChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Income', 'Expenses', 'Savings'],
            datasets: [{
                label: 'Amount (₹)',
                data: [
                    metrics.total_income,
                    metrics.total_expenses,
                    metrics.total_savings
                ],
                backgroundColor: [
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(239, 68, 68, 0.8)',
                    'rgba(59, 130, 246, 0.8)'
                ],
                borderColor: [
                    'rgba(16, 185, 129, 1)',
                    'rgba(239, 68, 68, 1)',
                    'rgba(59, 130, 246, 1)'
                ],
                borderWidth: 2,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return formatCurrency(context.parsed.y);
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#a0a0c0',
                        callback: function (value) {
                            return '₹' + value.toLocaleString('en-IN');
                        }
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    }
                },
                x: {
                    ticks: {
                        color: '#a0a0c0'
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// ===== Tab Switching =====
function handleTabSwitch(e) {
    const targetTab = e.target.dataset.tab;

    // Update active tab button
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    e.target.classList.add('active');

    // Show/hide tables
    if (targetTab === 'expenses') {
        document.getElementById('expensesTable').style.display = 'table';
        document.getElementById('incomesTable').style.display = 'none';
    } else {
        document.getElementById('expensesTable').style.display = 'none';
        document.getElementById('incomesTable').style.display = 'table';
    }
}

// ===== Utility Functions =====
function formatCurrency(amount) {
    return '₹' + amount.toLocaleString('en-IN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function generateColors(count) {
    const colors = [
        '#667eea', '#764ba2', '#f093fb', '#f5576c',
        '#4facfe', '#00f2fe', '#43e97b', '#38f9d7',
        '#fa709a', '#fee140', '#30cfd0', '#330867',
        '#a8edea', '#fed6e3', '#ff9a9e', '#fecfef'
    ];

    return colors.slice(0, count);
}

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast show ${type}`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
