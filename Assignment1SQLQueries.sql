show databases;

use hsbc_bank;

show tables;

desc employees;

desc payroll;

select * from employees;

select employee_id, first_name, last_name from employees;

select distinct designation from employees;

select distinct location from departments;

select department_name, annual_budget from departments;

select * from employees order by employee_id limit 10;

select concat(first_name,'',last_name) as full_name from employees;

select concat(first_name,' ',last_name) as employee_name,
base_salary*12 as annualized_base_salary
from employees;

select project_name, project_status, budget from projects;

select payroll_id,
employee_id,
pay_month,
basic_pay,
bonus,
allowances,
deductions,
net_pay,
payment_status,
basic_pay+bonus+allowances-deductions as calculated_net_pay
from payroll;

select * from employees where base_salary > 90000;

select * from employees where base_salary between 60000 and 110000;

select * from employees where hire_date >= '2024-01-01';

select * from employees where employment_status = 'Active';

select * from employees where first_name like 'A%';

select * from employees where last_name like '%a%';

select * from employees where department_id in (1,3,5);

select * from employees where manager_id is null;

select * from employees order by base_salary desc;

select * from employees order by base_salary desc limit 5;

select * from projects where end_date is null;

select * from projects where budget > 7000000;

select * from payroll where payment_status = 'Pending';

select * from employees
where hire_date between '2025-01-01' and '2025-12-31';

select upper(concat(first_name,' ',last_name)) as employee_name
from employees;

select first_name,
length(first_name) as name_length
from employees;

select employee_id,
first_name,
year(hire_date) as hire_year
from employees;

select employee_id,
first_name,
round(base_salary,-3) as rounded_salary
from employees;

select * from employees
where designation in ('Analyst','Associate');

select * from employees
where employment_status='Active'
order by department_id, base_salary desc;

select count(*) from employees;

select employment_status,
count(employee_id) as emp_count
from employees
group by employment_status;

select min(base_salary) as min_salary,
max(base_salary) as max_salary,
avg(base_salary) as average_salary
from employees;

select sum(base_salary) as total_salary
from employees;

select department_id,
count(employee_id)
from employees
group by department_id;

select department_id,
avg(base_salary) as average_base_salary
from employees
group by department_id;

select department_id,
max(base_salary) as max_base_salary
from employees
group by department_id;

select department_id
from employees
group by department_id
having count(employee_id) > 4;

select department_id,
avg(base_salary)
from employees
group by department_id
having avg(base_salary) > 80000;

select designation,
count(employee_id)
from employees
group by designation;

select designation
from employees
group by designation
having count(employee_id) >= 3;

select pay_month,
sum(net_pay)
from payroll
group by pay_month;

select pay_month,
sum(bonus)
from payroll
group by pay_month;

select pay_month,
payment_status,
count(*)
from payroll
group by pay_month,payment_status;

select project_status,
avg(budget)
from projects
group by project_status;

select project_status,
count(project_id)
from projects
group by project_status;

select project_status
from projects
group by project_status
having count(project_id) > 1;

select department_id
from employees
group by department_id
having max(base_salary) > 120000;

select concat(first_name,' ',last_name) as employee_name,
department_name
from employees e
inner join departments d
on e.department_id = d.department_id;

select concat(first_name,' ',last_name) as employee_name,
designation,
location
from employees e
inner join departments d
on e.department_id = d.department_id;

select concat(first_name,' ',last_name) as employee_name
from employees e
inner join departments d
on e.department_id = d.department_id
where department_name = 'Technology';

select concat(first_name,' ',last_name) as employee_name,
department_name,
base_salary
from employees e
inner join departments d
on e.department_id = d.department_id
order by base_salary;

select department_name,
count(employee_id) as employee_count
from employees e
inner join departments d
on e.department_id = d.department_id
group by department_name;

select department_name,
avg(base_salary) as employee_salary
from employees e
inner join departments d
on e.department_id = d.department_id
group by department_name;

select d.department_name,
count(employee_id) as employee_count
from employees e
inner join departments d
on e.department_id = d.department_id
group by department_name
having count(employee_id) >= 5;

select concat(first_name,' ',last_name) as employee_name,
pay_month,
net_pay
from employees e
inner join payroll p
on e.employee_id = p.employee_id;

select concat(first_name,' ',last_name) as employee_name
from employees e
inner join payroll p
on e.employee_id = p.employee_id
where p.pay_month = '2026-10-01'
and p.payment_status = 'Pending';

select e.first_name,
e.last_name,
p.bonus
from employees e
join payroll p
on e.employee_id = p.employee_id
where p.pay_month = '2026-09-01';

select e.employee_id,
e.first_name,
e.last_name,
sum(p.net_pay) as total_net_pay
from employees e
join payroll p
on e.employee_id = p.employee_id
group by e.employee_id,e.first_name,e.last_name;

select e.employee_id,
e.first_name,
e.last_name,
sum(p.net_pay) as total_net_pay
from employees e
join payroll p
on e.employee_id = p.employee_id
group by e.employee_id,e.first_name,e.last_name
order by total_net_pay desc
limit 5;

select p.project_name,
ep.role_on_project
from employeeprojects ep
join projects p
on ep.project_id = p.project_id;

select e.first_name,
e.last_name,
ep.allocation_pct
from employees e
join employeeprojects ep
on e.employee_id = ep.employee_id;

select p.project_name,
count(ep.employee_id) as emp_count
from projects p
join employeeprojects ep
on p.project_id = ep.project_id
group by p.project_id,p.project_name;

select p.project_name,
ep.employee_id
from projects p
left join employeeprojects ep
on p.project_id = ep.project_id;

select e.employee_id,
e.first_name,
e.last_name
from employees e
left join employeeprojects ep
on e.employee_id = ep.employee_id
where ep.employee_id is null;

select e.first_name as employee_name,
m.first_name as manager_name
from employees e
join employees m
on e.manager_id = m.employee_id;

select e.first_name as employee_name,
m.first_name as manager_name
from employees e
left join employees m
on e.manager_id = m.employee_id;

select e.employee_id,
e.first_name,
e.base_salary,
m.first_name as manager_name,
m.base_salary as manager_salary
from employees e
join employees m
on e.manager_id = m.employee_id
where e.base_salary > m.base_salary;

select e.first_name,
d.department_name,
p.pay_month,
p.net_pay
from employees e
join departments d
on e.department_id = d.department_id
join payroll p
on e.employee_id = p.employee_id;

select d.department_name,
sum(p.net_pay) as total_oct_payroll
from departments d
join employees e
on d.department_id = e.department_id
join payroll p
on e.employee_id = p.employee_id
where p.pay_month = '2026-10-01'
group by d.department_name;

select d.department_name,
sum(p.net_pay) as total_oct_payroll
from departments d
join employees e
on d.department_id = e.department_id
join payroll p
on e.employee_id = p.employee_id
where p.pay_month = '2026-10-01'
group by d.department_name
having sum(p.net_pay) > 500000;

select e.first_name,
e.last_name,
p.project_name,
ep.role_on_project
from employees e
join employeeprojects ep
on e.employee_id = ep.employee_id
join projects p
on ep.project_id = p.project_id;

select p.project_name,
e.first_name,
e.last_name
from projects p
join employeeprojects ep
on p.project_id = ep.project_id
join employees e
on ep.employee_id = e.employee_id
where p.project_status = 'Active';

select e.employee_id,
e.first_name,
count(distinct ep.project_id) as project_count
from employees e
join employeeprojects ep
on e.employee_id = ep.employee_id
group by e.employee_id,e.first_name;

select e.employee_id,
e.first_name,
count(ep.project_id) as project_count
from employees e
join employeeprojects ep
on e.employee_id = ep.employee_id
group by e.employee_id,e.first_name
having count(ep.project_id) >= 2;

select d.department_name,
count(distinct ep.project_id) as total_projects
from departments d
join employees e
on d.department_id = e.department_id
join employeeprojects ep
on e.employee_id = ep.employee_id
group by d.department_name;

select e.employee_id,
e.first_name,
e.base_salary,
e.department_id
from employees e
where e.base_salary =
(
select max(base_salary)
from employees e2
where e2.department_id = e.department_id
);

select *
from employees
where base_salary >
(
select avg(base_salary)
from employees
);

select *
from employees e
where base_salary >
(
select avg(base_salary)
from employees e2
where e2.department_id = e.department_id
);

select *
from projects
where budget >
(
select avg(budget)
from projects
);

select *
from employees e
where not exists
(
select 1
from payroll p
where p.employee_id = e.employee_id
and p.bonus > 0
);

select *
from employees e
where exists
(
select 1
from payroll p
where p.employee_id = e.employee_id
and p.payment_status = 'Pending'
);

select *
from employees e
where exists
(
select 1
from employeeprojects ep
join projects p
on ep.project_id = p.project_id
where ep.employee_id = e.employee_id
and p.budget > 8000000
);

select employee_id,
first_name,
base_salary,
case
when base_salary >= 100000 then 'High'
when base_salary >= 70000 then 'Medium'
else 'Low'
end as salary_category
from employees;

select project_id,
project_name,
budget,
case
when budget >= 8000000 then 'Large'
else 'Standard'
end as budget_category
from projects;

with cte as
(
select employee_id,
sum(net_pay) as total_net_pay
from payroll
group by employee_id
)
select *
from cte
order by total_net_pay desc
limit 10;

with cte as
(
select department_id,
avg(base_salary) as avg_salary
from employees
group by department_id
)
select *
from cte
where avg_salary >
(
select avg(base_salary)
from employees
);

select d.department_name,
count(distinct e.employee_id) as employee_count,
avg(e.base_salary) as avg_salary,
coalesce(sum(p.net_pay),0) as october_payroll
from departments d
left join employees e
on d.department_id = e.department_id
left join payroll p
on e.employee_id = p.employee_id
and p.pay_month = '2026-10-01'
group by d.department_id,d.department_name;

select p.project_name,
count(ep.employee_id) as total_employees
from projects p
join employeeprojects ep
on p.project_id = ep.project_id
group by p.project_id,p.project_name
order by total_employees desc
limit 1;

select e.employee_id,
e.first_name,
sum(ep.allocation_pct) as total_allocation
from employees e
join employeeprojects ep
on e.employee_id = ep.employee_id
group by e.employee_id,e.first_name
having sum(ep.allocation_pct) > 100;

with dept_avg as
(
select e.department_id,
avg(p.net_pay) as avg_net_pay
from employees e
join payroll p
on e.employee_id = p.employee_id
where p.pay_month = '2026-10-01'
group by e.department_id
)
select e.first_name,
d.department_name,
p.net_pay,
da.avg_net_pay
from employees e
join departments d
on e.department_id = d.department_id
join payroll p
on e.employee_id = p.employee_id
join dept_avg da
on e.department_id = da.department_id
where p.pay_month = '2026-10-01';

select d.department_name
from departments d
where not exists
(
select 1
from employees e
join employeeprojects ep
on e.employee_id = ep.employee_id
join projects p
on ep.project_id = p.project_id
where e.department_id = d.department_id
and p.project_status = 'Active'
);

select employee_id,
first_name,
department_id,
base_salary,
dense_rank() over
(
partition by department_id
order by base_salary desc
) as salary_rank
from employees;
